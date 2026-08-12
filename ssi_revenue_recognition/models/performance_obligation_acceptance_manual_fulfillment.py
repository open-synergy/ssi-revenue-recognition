# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PerformanceObligationAcceptanceManualFulfillment(models.Model):
    """
    One manually entered fulfillment line of a Performance Obligation
    Acceptance. Used when the fulfillment quantity of the parent
    acceptance is captured line by line rather than derived
    automatically.
    """

    _name = "performance_obligation_acceptance_manual_fulfillment"
    _description = "Performance Obligation Acceptance Manual Fulfillment"
    _inherit = [
        "mixin.product_line",
    ]

    acceptance_id = fields.Many2one(
        string="# Performance Obligation Acceptance",
        comodel_name="performance_obligation_acceptance",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        related="acceptance_id.performance_obligation_id.product_id",
        store=True,
    )
