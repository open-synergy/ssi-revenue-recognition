# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PerformanceObligationAcceptanceManualFulfillment(models.Model):
    _name = "performance_obligation_acceptance_manual_fulfillment"
    _description = "Performance Obligation Acceptance Manual Fulfillment"
    _inherit = [
        "mixin.product_line_price",
    ]

    detail_id = fields.Many2one(
        string="Acceptance Detail",
        comodel_name="performance_obligation_acceptance_detail",
        required=True,
        ondelete="cascade",
    )
