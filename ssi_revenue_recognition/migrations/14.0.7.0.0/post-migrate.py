# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Post-migration for 14.0.7.0.0.

    Recompute the stored ``amount_total_pob`` / ``amount_diff_pob`` on analytic
    accounts now that the PoB table is named ``performance_obligation`` and the
    ``source_analytic_account_id`` relationship is in place. Idempotent and safe
    on environments without PoB data.
    """
    _logger.info("14.0.7.0.0 post-migrate: recompute analytic PoB totals")

    openupgrade.logged_query(
        cr,
        """
        UPDATE account_analytic_account aa
        SET amount_total_pob = sub.total,
            amount_diff_pob  = COALESCE(aa.pob_planned_amount, 0.0) - sub.total
        FROM (
            SELECT source_analytic_account_id AS aa_id,
                   COALESCE(SUM(price_subtotal), 0.0) AS total
            FROM performance_obligation
            WHERE source_analytic_account_id IS NOT NULL
            GROUP BY source_analytic_account_id
        ) sub
        WHERE aa.id = sub.aa_id
        """,
    )

    _logger.info("14.0.7.0.0 post-migrate: done")
