# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RevenueRecognitionTypeAccount(models.Model):
    """
    One default WIP/expense account mapping line of a
    ``revenue_recognition_type``. Copied onto a new
    ``revenue_recognition`` document's ``account_ids`` when the type
    is selected (see ``revenue_recognition.onchange_account_ids``).
    """

    _name = "revenue_recognition_type_account"
    _description = "Revenue Recognition Type Account Mapping"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="revenue_recognition_type",
        required=True,
        ondelete="cascade",
    )
    wip_account_id = fields.Many2one(
        string="WIP Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
    )
    expense_account_id = fields.Many2one(
        string="Expense Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
    )
