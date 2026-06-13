# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_OLD_TABLE = "service_contract_performance_obligation"
_NEW_TABLE = "performance_obligation"

# service.contract / service.type column-bearing fields that used to be defined
# by ssi_revenue_recognition and are now owned by the ssi_service_revenue_recognition
# bridge. Their ir.model.data ownership is reassigned to the bridge BEFORE the
# schema is reflected, so that _process_end does not treat them as orphans and
# DROP the columns (data loss) while the bridge is not yet installed.
#
# Idempotent / environment-agnostic: in environments where the bridge is already
# installed and already owns these xmlids, the UPDATE simply matches zero rows.
_FIELD_XMLIDS_TO_BRIDGE = (
    "field_service_contract__pob_analytic_group_id",
    "field_service_contract__analytic_budget_id",
    "field_service_contract__lock_budget",
    "field_service_contract__amount_total_pob",
    "field_service_contract__amount_diff_pob",
    "field_service_type__pob_analytic_group_id",
    "field_service_type__auto_create_pob_product_ids",
    "field_service_type__auto_create_pob_product_categ_ids",
    # non-stored (no column) but reassigned for cleanliness / no churn
    "field_service_contract_fix_item__pob_id",
)


def migrate(cr, version):
    """Pre-migration for 14.0.7.0.0.

    Final structural step of the service-contract decoupling, isolated in its
    own version so it runs in EVERY environment that has not seen it yet
    (whether upgrading from 14.0.4.x or from an interim 14.0.6.0.0 build):

    1. Rename the physical PoB table to ``performance_obligation`` (the model
       ``_table`` override has been removed in code, so the default table name
       must exist before reflection).
    2. Hand off ownership of the service.contract / service.type glue fields to
       the ssi_service_revenue_recognition bridge so the columns survive the
       orphan cleanup when the bridge is not installed in the same run.

    Runs before the single schema reflection of this upgrade.
    """
    _logger.info("14.0.7.0.0 pre-migrate: start")

    # ------------------------------------------------------------------
    # 1. Rename the physical table (idempotent). openupgrade.rename_tables
    #    also renames the id sequence, indexes and constraints. Postgres FKs
    #    follow the rename automatically (they reference the table OID).
    # ------------------------------------------------------------------
    if openupgrade.table_exists(cr, _OLD_TABLE) and not openupgrade.table_exists(
        cr, _NEW_TABLE
    ):
        openupgrade.rename_tables(cr, [(_OLD_TABLE, _NEW_TABLE)])
        _logger.info(
            "14.0.7.0.0 pre-migrate: renamed table %s -> %s",
            _OLD_TABLE,
            _NEW_TABLE,
        )
    else:
        _logger.info(
            "14.0.7.0.0 pre-migrate: table rename skipped (already done or absent)"
        )

    # ------------------------------------------------------------------
    # 2. Field ownership handoff to ssi_service_revenue_recognition.
    #    Idempotent: a re-run (or an environment where the bridge already owns
    #    the xmlids) matches zero rows.
    # ------------------------------------------------------------------
    openupgrade.logged_query(
        cr,
        """
        UPDATE ir_model_data
        SET module = 'ssi_service_revenue_recognition'
        WHERE module = 'ssi_revenue_recognition'
          AND model = 'ir.model.fields'
          AND name IN %s
        """,
        (_FIELD_XMLIDS_TO_BRIDGE,),
    )

    _logger.info("14.0.7.0.0 pre-migrate: done")
