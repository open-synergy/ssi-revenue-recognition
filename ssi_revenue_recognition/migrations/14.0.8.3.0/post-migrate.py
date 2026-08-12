# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Post-migration for 14.0.8.3.0.

    Backfill ``parent_id`` on every analytic account owned by a
    Performance Obligation so it sits directly below the analytic
    account of its contract (``source_analytic_account_id``).

    Until this version ``performance_obligation._prepare_analytic_account``
    left ``parent_id`` empty, so each PoB analytic account was created as
    a root and the "contract analytic account -> PoB analytic account"
    hierarchy never existed for existing data.

    Written through the ORM on purpose -- not with
    ``openupgrade.logged_query`` like the earlier migrations of this
    module -- because ``account.analytic.account.complete_name`` is a
    stored compute and OCA ``account_analytic_parent`` maintains
    ``parent_path``; neither is refreshed by raw SQL writes.

    Idempotent and conditional: only PoBs that have both an analytic
    account and a source analytic account, that are not the very same
    record, and whose analytic account does not already point at that
    source, are written.  Re-running the script matches nothing.

    :param cr: database cursor
    :param version: version the module is upgraded from
    """
    _logger.info("14.0.8.3.0 post-migrate: backfill PoB analytic parent")

    env = api.Environment(cr, SUPERUSER_ID, {})
    obligations = env["performance_obligation"].search(
        [
            ("analytic_account_id", "!=", False),
            ("source_analytic_account_id", "!=", False),
        ]
    )
    to_backfill = obligations.filtered(
        lambda pob: pob.analytic_account_id != pob.source_analytic_account_id
        and pob.analytic_account_id.parent_id != pob.source_analytic_account_id
    )

    counter = 0
    for source in to_backfill.mapped("source_analytic_account_id"):
        accounts = to_backfill.filtered(
            lambda pob, source=source: pob.source_analytic_account_id == source
        ).mapped("analytic_account_id")
        accounts.write({"parent_id": source.id})
        counter += len(accounts)

    _logger.info(
        "14.0.8.3.0 post-migrate: done, %s analytic account(s) reparented",
        counter,
    )
