# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Post-migration for ssi_revenue_recognition_operating_unit 14.0.3.1.0.

    Defensive recompute of performance_obligation_acceptance.operating_unit_id.

    The field changed from related("contract_id.operating_unit_id") to
    related("performance_obligation_id.operating_unit_id", store=True) during the
    revenue-recognition decoupling. For existing acceptance rows the stored value
    normally already matches (the acceptance OU equalled the contract OU, which
    equals the now-preserved PoB OU), but we realign it explicitly so the
    "Responsible to operating unit data" record rule never shows a stale OU on
    instances that carry acceptance records.

    Runs after the single schema reflection; the PoB table is already named
    "performance_obligation" (renamed by ssi_revenue_recognition, a dependency
    that loads first). Idempotent: only touches rows where the value differs.
    """
    _logger.info(
        "14.0.3.1.0 post-migrate: realign acceptance.operating_unit_id from PoB"
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE performance_obligation_acceptance poa
        SET operating_unit_id = pob.operating_unit_id
        FROM performance_obligation pob
        WHERE poa.performance_obligation_id = pob.id
          AND poa.operating_unit_id IS DISTINCT FROM pob.operating_unit_id
        """,
    )
    _logger.info("14.0.3.1.0 post-migrate: done")
