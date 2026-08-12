# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RevenueRecognitionAccount(models.Model):
    """
    One WIP/expense account mapping line of a ``revenue_recognition``
    document. Tracks the debit/credit posted to its ``wip_account_id``
    for the period, the budget available on its ``expense_account_id``,
    and posts the corresponding expense/WIP accounting entries.
    """

    _name = "revenue_recognition_account"
    _description = "Revenue Recognition Account Mapping"

    recognition_id = fields.Many2one(
        string="# Recognition",
        comodel_name="revenue_recognition",
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
    company_currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="recognition_id.company_currency_id",
    )
    debit = fields.Monetary(
        string="Debit",
        required=True,
        currency_field="company_currency_id",
        default=0.0,
    )
    credit = fields.Monetary(
        string="Credit",
        required=True,
        currency_field="company_currency_id",
        default=0.0,
    )
    balance = fields.Monetary(
        string="Balance",
        currency_field="company_currency_id",
        compute="_compute_balance",
        store=True,
    )
    budget = fields.Monetary(
        string="Budget",
        required=True,
        currency_field="company_currency_id",
        default=0.0,
    )
    theoritical_balance = fields.Monetary(
        string="Theoritical Balance",
        currency_field="company_currency_id",
        compute="_compute_theoritical_balance",
        store=True,
    )
    percent_realized = fields.Float(
        string="Percent Realized",
        compute="_compute_percent_realized",
        store=True,
    )
    debit_move_line_id = fields.Many2one(
        string="Debit Move Line",
        comodel_name="account.move.line",
        readonly=True,
    )
    credit_move_line_id = fields.Many2one(
        string="Credit Move Line",
        comodel_name="account.move.line",
        readonly=True,
    )

    @api.depends(
        "debit",
        "credit",
    )
    def _compute_balance(self):
        """Derive the net balance of this account mapping line.

        Simply ``debit`` minus ``credit``.
        """
        for record in self:
            record.balance = record.debit - record.credit

    @api.depends(
        "balance",
        "budget",
    )
    def _compute_percent_realized(self):
        """Derive the realized percentage against the budget.

        ``balance`` divided by ``budget``, expressed as a percentage.
        Stays zero when there is no budget to divide by.
        """
        for record in self:
            percent_realized = 0.0
            if record.budget:
                percent_realized = record.balance / record.budget
            record.percent_realized = percent_realized * 100.00

    @api.depends("budget", "recognition_id.percentage_accepted")
    def _compute_theoritical_balance(self):
        """Derive the balance implied by the PoB's accepted percentage.

        Multiplies ``budget`` by the parent recognition's
        ``percentage_accepted``, used as an alternative expense
        amount policy (``theoritical_balance``) to the actually
        posted ``balance``.
        """
        for record in self:
            record.theoritical_balance = (
                record.recognition_id.percentage_accepted / 100.00
            ) * record.budget

    def _create_expense_ml(self):
        """Create the expense move line for this account mapping line.

        Called by ``revenue_recognition._create_expense_ml`` for each
        line.
        """
        self.ensure_one()
        ML = self.env["account.move.line"]
        ML.with_context(check_move_validity=False).create(self._prepare_expense_ml())

    def _prepare_expense_ml(self):
        """Build the debit move line values for the expense account.

        Debits ``expense_account_id`` with the amount selected by the
        parent recognition's ``expense_amount_policy`` (``balance``
        or ``theoritical_balance``).

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        return self._prepare_ml(
            account=self.expense_account_id,
            debit=getattr(self, self.recognition_id.expense_amount_policy),
            credit=0.0,
        )

    def _create_wip_ml(self):
        """Create the WIP move line for this account mapping line.

        Called by ``revenue_recognition._create_wip_ml`` for each
        line.
        """
        self.ensure_one()
        ML = self.env["account.move.line"]
        ML.with_context(check_move_validity=False).create(self._prepare_wip_ml())

    def _prepare_wip_ml(self):
        """Build the credit move line values for the WIP account.

        Credits ``wip_account_id`` with the same amount debited to
        the expense account, releasing the WIP as expense is
        recognised.

        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        return self._prepare_ml(
            account=self.wip_account_id,
            credit=getattr(self, self.recognition_id.expense_amount_policy),
            debit=0.0,
        )

    def _prepare_ml(self, account, debit, credit):
        """Build the common ``account.move.line`` values for this line.

        Shared by ``_prepare_expense_ml``/``_prepare_wip_ml``: sets
        the account, the PoB's partner, the PoB's own analytic
        account, and the given debit/credit onto the parent
        recognition's ``move_id``.

        :param account: an ``account.account`` record
        :param debit: debit amount
        :param credit: credit amount
        :return: dict of ``account.move.line`` values
        """
        pob = self.recognition_id.performance_obligation_id
        return {
            "account_id": account.id,
            "partner_id": pob.partner_id.id,
            "analytic_account_id": pob.analytic_account_id.id,
            "debit": debit,
            "credit": credit,
            "move_id": self.recognition_id.move_id.id,
        }
