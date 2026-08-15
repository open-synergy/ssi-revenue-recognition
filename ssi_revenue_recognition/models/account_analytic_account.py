# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    """
    Adds PSAK 115 / IFRS 15 revenue recognition attributes to the
    analytic account acting as a contract, and aggregates the totals
    of the Performance Obligations (PoB) generated from it.
    """

    _name = "account.analytic.account"
    _inherit = ["account.analytic.account"]

    revenue_recognition_type = fields.Selection(
        string="Revenue Recognition Type",
        selection=[
            ("full", "Full"),
            ("periodic", "Periodic"),
        ],
    )
    progress_completion_method = fields.Selection(
        string="Progress Completion Method",
        selection=[
            ("input", "Input"),
            ("output", "Output"),
        ],
        required=True,
        default="input",
    )
    pob_planned_amount = fields.Monetary(
        string="PoB Planned Amount",
        currency_field="currency_id",
        default=0.0,
    )
    pob_ids = fields.One2many(
        string="Performance Obligations",
        comodel_name="performance_obligation",
        inverse_name="source_analytic_account_id",
        readonly=True,
    )
    amount_total_pob = fields.Monetary(
        string="Total Performance Obligation",
        currency_field="currency_id",
        compute="_compute_amount_pob",
        store=True,
    )
    amount_diff_pob = fields.Monetary(
        string="PoB Diff.",
        currency_field="currency_id",
        compute="_compute_amount_pob",
        store=True,
    )

    @api.depends("pob_ids", "pob_ids.price_subtotal", "pob_planned_amount")
    def _compute_amount_pob(self):
        """Aggregate PoB amounts against the planned contract amount.

        ``amount_total_pob`` sums ``price_subtotal`` of every child
        ``performance_obligation``; ``amount_diff_pob`` is the gap
        between ``pob_planned_amount`` and that sum, so a positive
        value means the contract still has unallocated amount left.
        """
        for record in self:
            total = sum(p.price_subtotal for p in record.pob_ids)
            record.amount_total_pob = total
            record.amount_diff_pob = record.pob_planned_amount - total
