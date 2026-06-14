# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Post-migration for ssi_revenue_recognition_operating_unit 14.0.3.2.0.

    Defensive fill of revenue_recognition.operating_unit_id from its performance
    obligation. The field is newly added as a stored related on
    performance_obligation_id.operating_unit_id so that performance obligation,
    acceptance, and revenue recognition always share the same operating unit.
    Odoo computes the stored related for existing rows during the module update;
    this realign is an idempotent safety net that only touches rows whose stored
    value differs from the performance obligation.
    """
    _logger.info(
        "14.0.3.2.0 post-migrate: fill revenue_recognition.operating_unit_id from PoB"
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE revenue_recognition rr
        SET operating_unit_id = pob.operating_unit_id
        FROM performance_obligation pob
        WHERE rr.performance_obligation_id = pob.id
          AND rr.operating_unit_id IS DISTINCT FROM pob.operating_unit_id
        """,
    )
    _logger.info("14.0.3.2.0 post-migrate: done")
