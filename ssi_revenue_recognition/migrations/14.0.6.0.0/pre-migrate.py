# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_STALE_VIEW_MODELS = (
    "service.contract",
    "service.type",
    "service.contract_fix_item",
    "service_contract.performance_obligation",
)


def migrate(cr, version):
    """Pre-migration for 14.0.6.0.0.

    Delete stale views for models no longer managed by this module (the
    service.contract / service.type form extensions moved to the bridge
    modules). Recursively removes child views inherited by other modules to
    satisfy the FK constraint.

    NOTE: the physical-table rename and the field-ownership handoff were
    intentionally moved to 14.0.7.0.0 -- version 14.0.6.0.0 was already applied
    in some environments (e.g. dev) with a different meaning, so reusing it for
    new destructive operations would skip them there.
    """
    _logger.info("14.0.6.0.0 pre-migrate: start (stale view cleanup)")

    cr.execute(
        """
        SELECT v.id
        FROM ir_ui_view v
        JOIN ir_model_data d ON d.res_id = v.id AND d.model = 'ir.ui.view'
        WHERE d.module = 'ssi_revenue_recognition'
          AND v.model = ANY(%s)
        """,
        (list(_STALE_VIEW_MODELS),),
    )
    stale_ids = [r[0] for r in cr.fetchall()]
    if not stale_ids:
        _logger.info("14.0.6.0.0 pre-migrate: no stale views, nothing to do")
        return

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
        (stale_ids,),
    )
    all_ids = [r[0] for r in cr.fetchall()]
    if all_ids:
        openupgrade.logged_query(
            cr,
            "DELETE FROM ir_model_data WHERE model = 'ir.ui.view' AND res_id = ANY(%s)",
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
            (stale_ids,),
        )

    _logger.info("14.0.6.0.0 pre-migrate: done")
