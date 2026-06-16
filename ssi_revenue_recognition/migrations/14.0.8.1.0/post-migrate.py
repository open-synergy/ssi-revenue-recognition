# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Post-migration for 14.0.8.1.0.

    Resync the stored-related ``approval_template.model`` Char column with
    ``ir_model.model`` for the ``performance_obligation`` model.

    When the model was renamed from ``service_contract.performance_obligation``
    to ``performance_obligation`` in migration 14.0.5.0.0, openupgradelib's
    ``rename_models`` updated ``ir_model.model`` via raw SQL.  Stored related
    fields are not recomputed by raw SQL writes, so ``approval_template.model``
    still held the old name.  As a result, ``action_request_approval()``
    searched ``[("model", "=", "performance_obligation")]`` and found zero
    templates — silently skipping the approval step on PoB confirm.

    This script is idempotent: if the column is already in sync (e.g. on a
    fresh install where the old name never existed), the UPDATE matches zero
    rows and does nothing.
    """
    _logger.info("14.0.8.1.0 post-migrate: resync approval_template.model")

    openupgrade.logged_query(
        cr,
        """
        UPDATE approval_template at
        SET model = im.model
        FROM ir_model im
        WHERE at.model_id = im.id
          AND at.model != im.model
        """,
    )

    _logger.info("14.0.8.1.0 post-migrate: done")
