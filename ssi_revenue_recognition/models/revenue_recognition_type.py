# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RevenueRecognitionType(models.Model):
    _name = "revenue_recognition_type"
    _inherit = ["mixin.master_data"]
    _description = "Revenue Recognition Type"

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        ondelete="restrict",
    )
    account_ids = fields.One2many(
        string="Account Mappings",
        comodel_name="revenue_recognition_type_account",
        inverse_name="type_id",
    )
