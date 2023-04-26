# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PerformanceObligationAcceptanceDetail(models.Model):
    _name = "performance_obligation_acceptance_detail"
    _description = "Performance Obligation Acceptance Detail"

    acceptance_id = fields.Many2one(
        string="# Acceptance",
        comodel_name="performance_obligation_acceptance",
        required=True,
        ondelete="cascade",
    )
    budget_detail_id = fields.Many2one(
        string="Budget Detail",
        comodel_name="analytic_budget.detail",
        required=True,
        readonly=True,
    )
    name = fields.Char(
        string="Description",
        related="budget_detail_id.name",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="budget_detail_id.currency_id",
        store=True,
    )
    fullfilment_method = fields.Selection(
        string="Fullfilment Method",
        related="budget_detail_id.fullfilment_method",
        store=True,
    )
    amount_fulfilled = fields.Monetary(
        string="Amount Fulfilled",
        compute="_compute_amount_fulfilled",
        currency_field="currency_id",
        store=True,
    )

    # Manual Fulfillment
    manual_fulfillment_ids = fields.One2many(
        string="Manual Fulfillments",
        comodel_name="performance_obligation_acceptance_manual_fulfillment",
        inverse_name="detail_id",
    )
    amount_manual_fulfillment = fields.Float(
        string="Amount of Manual Fulfillmen",
        compute="_compute_amount_manual_fulfillment",
        store=True,
    )

    @api.depends(
        "manual_fulfillment_ids",
        "manual_fulfillment_ids.price_subtotal",
    )
    def _compute_amount_manual_fulfillment(self):
        for record in self:
            result = 0.0
            for manual_fulfillment in self.manual_fulfillment_ids:
                result += manual_fulfillment.price_subtotal
            record.amount_manual_fulfillment = result
            record._compute_amount_fulfilled()

    @api.depends(
        "fullfilment_method",
    )
    def _compute_amount_fulfilled(self):
        for record in self:
            try:
                result = getattr(record, record.fullfilment_method)
            except Exception:
                result = 0.0

            record.amount_fulfilled = result
