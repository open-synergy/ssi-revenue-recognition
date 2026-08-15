# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PerformanceObligationAcceptance(models.Model):
    """
    Bridges Performance Obligation Acceptance to ``hr.work_log`` via
    ``mixin.work_object``, and adds a curated selection layer on top
    of it. ``allowed_work_log_ids`` computes which logs are eligible
    to be picked, ``poa_work_log_ids`` holds the ones the user
    actually selects, and ``qty_work_log`` sums their duration into
    the quantity that feeds the acceptance's fulfilled quantity.
    """

    _name = "performance_obligation_acceptance"
    _inherit = [
        "performance_obligation_acceptance",
        "mixin.work_object",
    ]

    _work_log_create_page = True

    allowed_work_log_ids = fields.Many2many(
        string="Allowed Work Logs",
        comodel_name="hr.work_log",
        compute="_compute_allowed_work_log_ids",
        store=False,
    )
    poa_work_log_ids = fields.Many2many(
        string="Work Logs",
        comodel_name="hr.work_log",
        relation="rel_poa_2_work_log",
        column1="poa_id",
        column2="work_log_id",
    )
    qty_work_log = fields.Float(
        string="Work Qty",
        compute="_compute_qty_work_log",
        store=True,
    )

    @api.depends(
        "date_start",
        "date_end",
        "performance_obligation_id",
    )
    def _compute_allowed_work_log_ids(self):
        """Compute the ``hr.work_log`` records eligible for selection.

        Filters ``hr.work_log`` by the PoB's (``performance_obligation_id``)
        ``analytic_account_id``, restricted to the acceptance's
        ``date_start``/``date_end`` window and to logs in ``done``
        state, then stores the matching ids on
        ``allowed_work_log_ids``.
        """
        for record in self:
            pob = record.performance_obligation_id

            WorkLog = self.env["hr.work_log"]
            criteria = [
                ("analytic_account_id", "=", pob.analytic_account_id.id),
                ("date", ">=", record.date_start),
                ("date", "<=", record.date_end),
                ("state", "=", "done"),
            ]
            record.allowed_work_log_ids = WorkLog.search(criteria).ids

    @api.depends(
        "poa_work_log_ids",
        "poa_work_log_ids.amount",
    )
    def _compute_qty_work_log(self):
        """Sum the selected work logs' duration into ``qty_work_log``.

        Adds up the ``amount`` (``Duration``) field of every record
        in ``poa_work_log_ids`` — the work logs actually picked for
        this acceptance, out of ``allowed_work_log_ids`` — and stores
        the total, in the same unit as ``hr.work_log.amount``, on
        ``qty_work_log``. Also triggers recomputation of the
        acceptance's fulfilled quantity via
        ``_compute_qty_fulfilled``.
        """
        for record in self:
            result = 0.0
            for work_log in record.poa_work_log_ids:
                result += work_log.amount
            record.qty_work_log = result
            record._compute_qty_fulfilled()

    @api.constrains(
        "poa_work_log_ids",
    )
    def _check_poa_work_log_ids(self):
        """Reject work logs picked outside ``allowed_work_log_ids``.

        The ``domain=`` restriction on the ``poa_work_log_ids`` widget
        (``views/performance_obligation_acceptance_views.xml``) only
        filters what the UI shows — it does not stop ``write()``/
        ``create()`` performed through the ORM or RPC directly. This
        constraint re-checks the same membership on the server, so a
        work log outside the acceptance's ``allowed_work_log_ids``
        (wrong analytic account, date window, or not in ``done``
        state) can never end up counted in ``qty_work_log``.

        :raises ValidationError: when ``poa_work_log_ids`` contains at
            least one work log absent from ``allowed_work_log_ids``.
        """
        for record in self:
            disallowed = record.poa_work_log_ids - record.allowed_work_log_ids
            for work_log in disallowed:
                error_message = (
                    _(
                        """
Context: Select work log for %s
Database ID: %s
Problem: Work log "%s" is not part of the allowed work logs
Solution: Select work logs within the acceptance's date window and
matching the performance obligation's analytic account
"""
                    )
                    % (
                        record._description.lower(),
                        record.id,
                        work_log.description,
                    )
                )
                raise ValidationError(error_message)
