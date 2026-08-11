# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
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
    pob_cost_revenue_count = fields.Integer(
        string="# PoB Cost/Revenue",
        compute="_compute_pob_cost_revenue_count",
    )

    @api.depends("pob_ids", "pob_ids.price_subtotal", "pob_planned_amount")
    def _compute_amount_pob(self):
        for record in self:
            total = sum(p.price_subtotal for p in record.pob_ids)
            record.amount_total_pob = total
            record.amount_diff_pob = record.pob_planned_amount - total

    @api.depends("pob_ids.analytic_account_id")
    def _compute_pob_cost_revenue_count(self):
        """Count analytic lines posted to this AA's PoBs' own accounts.

        Each PoB gets its own dedicated analytic account once opened
        (see performance_obligation._10_create_analytic_account),
        separate from this source analytic account, so PoB revenue
        recognition entries never land here directly. This aggregates
        them for the PoB Cost/Revenue smart button.
        """
        AAL = self.env["account.analytic.line"]
        for record in self:
            pob_aa_ids = record.pob_ids.mapped("analytic_account_id").ids
            record.pob_cost_revenue_count = AAL.search_count(
                [("account_id", "in", pob_aa_ids)]
            )

    def action_open_pob_cost_revenue(self):
        """Open analytic lines across all PoBs' own analytic accounts.

        Complements the core 'Cost/Revenue' button, which only shows
        lines posted directly to this source analytic account.
        """
        self.ensure_one()
        return {
            "name": "PoB Cost/Revenue",
            "type": "ir.actions.act_window",
            "res_model": "account.analytic.line",
            "view_mode": "tree,form,graph,pivot",
            "domain": [
                ("account_id", "in", self.pob_ids.mapped("analytic_account_id").ids)
            ],
        }
