# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AnalyticBudgetDetail(models.Model):
    _name = "analytic_budget.detail"
    _inherit = "analytic_budget.detail"

    fullfilment_method = fields.Selection(
        string="Fullfilment Method",
        selection=[
            ("amount_manual_fulfillment", "Amount of Manual Fulfillment"),
        ],
        required=True,
        default="amount_manual_fulfillment",
    )
    amount_to_fulfill = fields.Float(
        string="Amount To Fullfil",
        compute="_compute_amount_to_fullfil",
        store=True,
    )
    amount_fulfilled = fields.Float(
        string="Amount Fulfilled",
        compute="_compute_amount_fulfilled",
        store=True,
    )
    percentage_fulfilled = fields.Float(
        string="Percentage Fulfilled",
        compute="_compute_amount_fulfilled",
        store=True,
    )
    amount_residual = fields.Float(
        string="Amount Residual",
        compute="_compute_amount_residual",
        store=True,
    )
    amount_manual_fulfillment = fields.Float(
        string="Amount of Manual Fulfillmen",
        compute="_compute_amount_manual_fulfillment",
        store=True,
    )
    poa_detail_ids = fields.One2many(
        string="Performance Obligation Acceptance Details",
        comodel_name="performance_obligation_acceptance_detail",
        inverse_name="budget_detail_id",
    )

    def _compute_amount_manual_fulfillment(self):
        for record in self:
            record.amount_manual_fulfillment = 0.0

    @api.depends(
        "price_subtotal",
    )
    def _compute_amount_to_fullfil(self):
        for record in self:
            record.amount_to_fulfill = record.price_subtotal

    @api.depends(
        "fullfilment_method",
        "amount_to_fulfill",
        "poa_detail_ids",
        "poa_detail_ids.amount_fulfilled",
    )
    def _compute_amount_fulfilled(self):
        for record in self:
            result = 0.0
            for detail in record.poa_detail_ids:
                result += detail.amount_fulfilled

            try:
                percentage = (result / record.amount_to_fulfill) * 100.00
            except Exception:
                percentage = 0.0
            record.amount_fulfilled = result
            record.percentage_fulfilled = percentage

    @api.depends(
        "amount_to_fulfill",
        "amount_fulfilled",
    )
    def _compute_amount_residual(self):
        for record in self:
            record.amount_residual = record.amount_to_fulfill - record.amount_fulfilled
