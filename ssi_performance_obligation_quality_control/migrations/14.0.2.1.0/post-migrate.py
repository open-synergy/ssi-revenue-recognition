# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Post-migration for ssi_performance_obligation_quality_control 14.0.2.1.0.

    Re-sync qc_worksheet.model_name with its model_id.

    qc_worksheet.model_name is a stored related on model_id.model. When the
    performance obligation model was renamed (service_contract.performance_obligation
    -> performance_obligation, by ssi_revenue_recognition migration 14.0.5.0.0),
    openupgrade.rename_models updated ir_model and the well-known model-name columns
    but did NOT recompute this arbitrary stored-related Char, so existing qc_worksheet
    rows kept the old model name. The mixin.qc_worksheet One2many filters on
    model_name, so those worksheets silently detached from their performance
    obligation. This realigns the stored column with the live ir_model name. It is
    general (re-syncs ANY drifted model_name, not just the performance obligation
    one) and idempotent (touches zero rows on an already-consistent database).
    """
    _logger.info(
        "14.0.2.1.0 post-migrate: re-sync qc_worksheet.model_name from ir_model"
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE qc_worksheet w
        SET model_name = m.model
        FROM ir_model m
        WHERE w.model_id = m.id
          AND w.model_name IS DISTINCT FROM m.model
        """,
    )
    _logger.info("14.0.2.1.0 post-migrate: done")
