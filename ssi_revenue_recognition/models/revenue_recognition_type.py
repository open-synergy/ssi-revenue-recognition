# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RevenueRecognitionType(models.Model):
    """
    Master data configuring how a ``revenue_recognition`` document
    posts its accounting entry: which journal to use, which product
    usage codes resolve the unearned income/income accounts, and the
    default WIP/expense account mappings offered to new documents.
    """

    _name = "revenue_recognition_type"
    _inherit = ["mixin.master_data"]
    _description = "Revenue Recognition Type"

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        ondelete="restrict",
    )
    unearned_income_usage_id = fields.Many2one(
        string="Unearned Income Usage",
        comodel_name="product.usage_type",
        required=True,
        ondelete="restrict",
    )
    income_usage_id = fields.Many2one(
        string="Income Usage",
        comodel_name="product.usage_type",
        required=True,
        ondelete="restrict",
    )
    account_ids = fields.One2many(
        string="Account Mappings",
        comodel_name="revenue_recognition_type_account",
        inverse_name="type_id",
    )
    wip_account_ids = fields.Many2many(
        string="WIP Accounts",
        comodel_name="account.account",
        compute="_compute_account",
    )
    expense_account_ids = fields.Many2many(
        string="Expense Accounts",
        comodel_name="account.account",
        compute="_compute_account",
    )

    @api.depends(
        "account_ids",
        "account_ids.wip_account_id",
        "account_ids.expense_account_id",
    )
    def _compute_account(self):
        """Collect distinct WIP/expense accounts from ``account_ids``.

        ``wip_account_ids``/``expense_account_ids`` are the set of
        accounts used across ``account_ids`` mapping lines, exposed
        so a ``revenue_recognition`` document can restrict its WIP
        move line search to this type's configured accounts.
        """
        for record in self:
            wip_accounts = expense_accounts = self.env["account.account"]
            if record.account_ids:
                wip_accounts = record.account_ids.mapped("wip_account_id")
                expense_accounts = record.account_ids.mapped("expense_account_id")
            record.wip_account_ids = wip_accounts.ids
            record.expense_account_ids = expense_accounts.ids
