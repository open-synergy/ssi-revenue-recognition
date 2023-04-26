# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class PerformanceObligationAcceptance(models.Model):
    _name = "performance_obligation_acceptance"
    _inherit = [
        "mixin.date_duration",
        "mixin.partner",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Performance Obligation Acceptance"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_required = True
    _date_end_required = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    contact_partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="performance_obligation_acceptance_detail",
        inverse_name="acceptance_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_fulfilled = fields.Float(
        string="Amount Fulfilled",
        compute="_compute_amount_fulfilled",
        store=True,
    )
    state = fields.Selection(
        string="State",
        default="draft",
        required=True,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
    )

    @api.depends(
        "detail_ids",
        "detail_ids.amount_fulfilled",
    )
    def _compute_amount_fulfilled(self):
        for record in self:
            result = 0.0
            for detail in self.detail_ids:
                result += detail.amount_fulfilled
            record.amount_fulfilled = result

    @api.model
    def _get_policy_field(self):
        res = super(PerformanceObligationAcceptance, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "analytic_account_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange(
        "partner_id",
    )
    def onchange_analytic_account_id(self):
        self.analytic_account_id = False

    def action_reload_detail(self):
        for record in self.sudo():
            record._reload_detail()

    def _reload_detail(self):
        self.ensure_one()
        BudgetDetail = self.env["analytic_budget.detail"]
        POBDetail = self.env["performance_obligation_acceptance_detail"]
        domain = self._prepare_detail_domain()
        self.detail_ids.unlink()
        for detail in BudgetDetail.search(domain):
            POBDetail.create(
                {
                    "acceptance_id": self.id,
                    "budget_detail_id": detail.id,
                }
            )

    def _prepare_detail_domain(self):
        self.ensure_one()
        return [
            ("analytic_account_id", "=", self.analytic_account_id.id),
            ("direction", "=", "revenue"),
        ]
