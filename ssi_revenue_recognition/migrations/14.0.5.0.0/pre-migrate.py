# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_OLD_MODEL = "service_contract.performance_obligation"
_NEW_MODEL = "performance_obligation"
# The physical PoB table is still the legacy name "service_contract_performance_obligation"
# at this stage; it is renamed to "performance_obligation" in the 14.0.7.0.0 pre-migration.


def migrate(cr, version):
    """Pre-migration for 14.0.5.0.0.

    Decouple performance obligation from service.contract:
    - Populate ``source_analytic_account_id`` (and other previously related
      fields) from the originating service contract while ``contract_id`` and
      the ``service_contract`` table are still present.
    - Rename the model ``service_contract.performance_obligation`` ->
      ``performance_obligation`` (registry metadata only; the physical table is
      renamed in 14.0.6.0.0).

    Everything runs against the ORIGINAL stored schema (Odoo reflects the new
    schema only once, after all pre-migrations of this upgrade have run).
    """
    _logger.info("14.0.5.0.0 pre-migrate: start")

    # ------------------------------------------------------------------
    # 0a. Drop stale ir.ui.view records owned by this module BEFORE Odoo
    #     validates views. The service.contract / service.type form
    #     extensions (and the old PoB views) are removed from this module and
    #     recreated by the bridge modules; leaving them would raise
    #     ValidationError because they reference fields that no longer belong
    #     to this module. Child views inherited by other modules are removed
    #     recursively to satisfy the FK constraint.
    # ------------------------------------------------------------------
    cr.execute(
        """
        SELECT res_id FROM ir_model_data
        WHERE module = 'ssi_revenue_recognition' AND model = 'ir.ui.view'
        """
    )
    parent_ids = [r[0] for r in cr.fetchall()]
    if parent_ids:
        cr.execute(
            """
            WITH RECURSIVE desc_views AS (
                SELECT id FROM ir_ui_view WHERE id = ANY(%s)
                UNION ALL
                SELECT v.id FROM ir_ui_view v
                JOIN desc_views d ON v.inherit_id = d.id
            )
            SELECT id FROM desc_views
            """,
            (parent_ids,),
        )
        all_ids = [r[0] for r in cr.fetchall()]
        if all_ids:
            openupgrade.logged_query(
                cr,
                "DELETE FROM ir_model_data "
                "WHERE model = 'ir.ui.view' AND res_id = ANY(%s)",
                (all_ids,),
            )
            openupgrade.logged_query(
                cr,
                """
                WITH RECURSIVE desc_views AS (
                    SELECT id FROM ir_ui_view WHERE id = ANY(%s)
                    UNION ALL
                    SELECT v.id FROM ir_ui_view v
                    JOIN desc_views d ON v.inherit_id = d.id
                )
                DELETE FROM ir_ui_view WHERE id IN (SELECT id FROM desc_views)
                """,
                (parent_ids,),
            )

    # ------------------------------------------------------------------
    # 0b. Add the new columns if they do not exist yet (idempotent).
    # ------------------------------------------------------------------
    cr.execute(
        "ALTER TABLE service_contract_performance_obligation "
        "ADD COLUMN IF NOT EXISTS source_analytic_account_id INTEGER"
    )
    cr.execute(
        "ALTER TABLE account_analytic_account "
        "ADD COLUMN IF NOT EXISTS pob_planned_amount NUMERIC"
    )

    # ------------------------------------------------------------------
    # 1. source_analytic_account_id <- service_contract.analytic_account_id
    # ------------------------------------------------------------------
    openupgrade.logged_query(
        cr,
        """
        UPDATE service_contract_performance_obligation pob
        SET source_analytic_account_id = sc.analytic_account_id
        FROM service_contract sc
        WHERE pob.contract_id = sc.id
          AND sc.analytic_account_id IS NOT NULL
          AND pob.source_analytic_account_id IS NULL
        """,
    )

    # ------------------------------------------------------------------
    # 2. date <- service_contract.date (was a related field)
    # ------------------------------------------------------------------
    openupgrade.logged_query(
        cr,
        """
        UPDATE service_contract_performance_obligation pob
        SET date = sc.date
        FROM service_contract sc
        WHERE pob.contract_id = sc.id
          AND pob.date IS NULL
          AND sc.date IS NOT NULL
        """,
    )

    # ------------------------------------------------------------------
    # 3. analytic_account.group_id <- service_contract.pob_analytic_group_id
    # ------------------------------------------------------------------
    openupgrade.logged_query(
        cr,
        """
        UPDATE account_analytic_account aa
        SET group_id = sc.pob_analytic_group_id
        FROM service_contract sc
        WHERE sc.analytic_account_id = aa.id
          AND sc.pob_analytic_group_id IS NOT NULL
          AND aa.group_id IS NULL
        """,
    )

    # ------------------------------------------------------------------
    # 4. analytic_account.pob_planned_amount <- service_contract.amount_untaxed
    # ------------------------------------------------------------------
    openupgrade.logged_query(
        cr,
        """
        UPDATE account_analytic_account aa
        SET pob_planned_amount = sc.amount_untaxed
        FROM service_contract sc
        WHERE sc.analytic_account_id = aa.id
          AND sc.amount_untaxed IS NOT NULL
          AND (aa.pob_planned_amount IS NULL OR aa.pob_planned_amount = 0)
        """,
    )

    # ------------------------------------------------------------------
    # 5. Rename the model (registry metadata: ir_model, ir_model_fields,
    #    ir_model_data, ir_model_relation, ir_rule, ...). The physical table
    #    is intentionally NOT renamed here; that happens in 14.0.6.0.0.
    # ------------------------------------------------------------------
    cr.execute("SELECT 1 FROM ir_model WHERE model = %s", (_OLD_MODEL,))
    if cr.fetchone():
        openupgrade.rename_models(cr, [(_OLD_MODEL, _NEW_MODEL)])
        _logger.info(
            "14.0.5.0.0 pre-migrate: renamed model %s -> %s",
            _OLD_MODEL,
            _NEW_MODEL,
        )

    # Anomaly log: PoB still without a source analytic account (expected for
    # contracts in draft/confirm where the analytic account was not created).
    cr.execute(
        "SELECT COUNT(*) FROM service_contract_performance_obligation "
        "WHERE source_analytic_account_id IS NULL"
    )
    null_count = cr.fetchone()[0]
    if null_count:
        _logger.warning(
            "14.0.5.0.0 pre-migrate: %d PoB rows still have NULL "
            "source_analytic_account_id (expected for non-open contracts).",
            null_count,
        )

    _logger.info("14.0.5.0.0 pre-migrate: done")
