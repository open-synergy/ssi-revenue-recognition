# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class PerformanceObligation(models.Model):
    """
    Represents one Performance Obligation (PoB) of a contract under
    PSAK 115 / IFRS 15: a distinct promised good or service whose revenue
    is recognised separately from the rest of the contract.
    Each PoB owns its own analytic account, created when the document is
    opened and placed below the contract's source analytic account, so
    cost and revenue stay traceable per obligation.
    """

    _name = "performance_obligation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.product_line_price",
    ]
    _description = "Performance Obligation"
    _order = "source_analytic_account_id, sequence, id"

    _automatically_insert_view_element = True

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Policy fields visibility
    _automatically_insert_open_policy_fields = False
    _automatically_insert_done_policy_fields = False

    # Button visibility
    _automatically_insert_done_button = False
    _automatically_insert_open_button = False

    # Sequence attribute
    _create_sequence_state = "open"

    _statusbar_visible_label = "draft,open,done"
    _policy_field_order = [
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
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
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    source_analytic_account_id = fields.Many2one(
        string="Source Analytic Account",
        comodel_name="account.analytic.account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="source_analytic_account_id.partner_id",
        store=True,
    )
    title = fields.Char(
        string="Title",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    product_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    uom_quantity = fields.Float(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    uom_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pricelist_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    price_unit = fields.Monetary(
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
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=False,
    )
    analytic_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Analytic Partner",
        related="analytic_account_id.partner_id",
        store=True,
    )
    progress_completion_method = fields.Selection(
        string="Progress Completion Method",
        selection=[
            ("input", "Input"),
            ("output", "Output"),
        ],
        required=True,
        default="input",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    revenue_recognition_timing = fields.Selection(
        string="Revenue Recognition Timing",
        selection=[
            ("over_time", "Over Time"),
            ("point_in_time", "At a Point in Time"),
        ],
        required=True,
        default="over_time",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Date Start",
    )
    date_end = fields.Date(
        string="Date End",
    )
    require_date = fields.Boolean(
        string="Require Date",
        compute="_compute_date_attribute",
        store=False,
    )
    readonly_date = fields.Boolean(
        string="Readonly Date",
        compute="_compute_date_attribute",
        store=False,
    )
    invisible_date = fields.Boolean(
        string="Invisible Date",
        compute="_compute_date_attribute",
        store=False,
    )
    fulfillment_field_id = fields.Many2one(
        string="Fulfillment Field",
        comodel_name="ir.model.fields",
        domain=[
            ("model_id.model", "=", "performance_obligation_acceptance"),
            ("ttype", "=", "float"),
            ("name", "!=", "qty_fulfilled"),
        ],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    acceptance_ids = fields.One2many(
        string="Performance Obligation Acceptances",
        comodel_name="performance_obligation_acceptance",
        inverse_name="performance_obligation_id",
        readonly=True,
        copy=False,
    )
    quantity_accepted = fields.Float(
        string="Quantity Accepted",
        compute="_compute_quantity_accepted",
        store=True,
    )
    quantity_diff = fields.Float(
        string="Quantity Diff.",
        compute="_compute_quantity_accepted",
        store=True,
    )
    percentage_accepted = fields.Float(
        string="Percentage Accepted",
        compute="_compute_quantity_accepted",
        store=True,
    )
    amount_accepted = fields.Monetary(
        string="Amount Accepted",
        compute="_compute_quantity_accepted",
        store=True,
        currency_field="currency_id",
    )
    sequence = fields.Integer(
        required=True,
        default=1,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends(
        "revenue_recognition_timing",
        "state",
    )
    def _compute_date_attribute(self):
        """Derive the visibility/requirement of ``date_start``/``date_end``.

        The dates are required and shown only when
        ``revenue_recognition_timing`` is ``point_in_time``; once the
        record leaves ``draft`` the dates become readonly regardless
        of the timing.
        """
        for record in self:
            required = invisible = readonly = False
            if record.revenue_recognition_timing == "point_in_time":
                required = True
            else:
                invisible = True

            if record.state != "draft":
                readonly = True
            record.require_date = required
            record.readonly_date = readonly
            record.invisible_date = invisible

    @api.depends(
        "quantity",
        "acceptance_ids",
        "acceptance_ids.state",
        "acceptance_ids.qty_fulfilled",
    )
    def _compute_quantity_accepted(self):
        """Aggregate accepted quantity from ``done`` acceptances.

        Sums ``qty_fulfilled`` of every acceptance in state ``done``,
        then derives ``quantity_diff`` (remaining quantity),
        ``percentage_accepted``, and ``amount_accepted`` (accepted
        share of ``price_subtotal``). Falls back to zero percentage
        and amount when ``quantity`` is zero, to avoid a division
        error.
        """
        for record in self:
            qty_accepted = qty_diff = percentage = amount_accepted = 0.0
            for acceptance in record.acceptance_ids.filtered(
                lambda r: r.state == "done"
            ):
                qty_accepted += acceptance.qty_fulfilled

            qty_diff = record.quantity - qty_accepted
            try:
                percentage = (qty_accepted / record.quantity) * 100.00
                amount_accepted = (
                    qty_accepted / record.quantity
                ) * record.price_subtotal
            except Exception:
                percentage = 0.0
            record.quantity_accepted = qty_accepted
            record.quantity_diff = qty_diff
            record.percentage_accepted = percentage
            record.amount_accepted = amount_accepted

    @api.onchange(
        "revenue_recognition_timing",
    )
    def onchange_date_start(self):
        self.date_start = False

    @api.onchange(
        "revenue_recognition_timing",
    )
    def onchange_date_end(self):
        self.date_end = False

    @api.onchange("product_id")
    def onchange_name(self):
        """No-op placeholder onchange for ``name`` on ``product_id`` change.

        ``name`` is assigned from the ``open`` sequence (see
        ``_create_sequence_state``), not derived from the product, so
        there is nothing to reset here. Kept as an explicit hook so a
        glue module can extend it without introducing a new
        ``@api.onchange("product_id")`` registration.
        """

    @api.onchange("product_id")
    def onchange_title(self):
        self.title = False
        if self.product_id:
            self.title = self.product_id.display_name

    def _get_analytic_group_id(self):
        """Resolve the analytic group for the PoB's own analytic account.

        Reuses the contract's ``group_id`` so the PoB analytic account
        stays in the same analytic group as
        ``source_analytic_account_id``.

        Extension point: override to assign a different group.

        :return: id of the ``account.analytic.group``, or ``False``
            when the source account has no group
        """
        self.ensure_one()
        return self.source_analytic_account_id.group_id.id or False

    def _get_analytic_parent_id(self):
        """Resolve the parent of the analytic account owned by this PoB.

        ``source_analytic_account_id`` -- the contract's own analytic
        account -- is the single source of truth for that parent: every
        analytic account a PoB owns sits directly below it in the
        ``account.analytic.account`` hierarchy, so ``complete_name`` and
        hierarchy-based analytic reports group each PoB under its
        contract instead of showing it as another root account.

        Returns ``False`` when no source account is set, and also when
        the source account *is* this PoB's own analytic account: OCA
        ``account_analytic_parent`` raises ``UserError`` on recursive
        hierarchies, so a record must never become its own parent.

        Extension point: override to place the PoB analytic account
        somewhere else in the hierarchy.

        :return: id of the parent ``account.analytic.account``, or
            ``False`` when the account has to stay a root
        """
        self.ensure_one()
        source = self.source_analytic_account_id
        if not source or source == self.analytic_account_id:
            return False
        return source.id

    @ssi_decorator.pre_open_check()
    def _10_check_open_source_state(self):
        """Block ``action_open`` when called from a state that is not
        allowed to open.

        ``_automatically_insert_open_button`` is ``False`` on this
        model, so ``_check_open_policy()`` returns early and never
        evaluates ``open_ok`` -- the ``draft -> open`` transition is
        gated by ``approval.template`` instead
        (``_after_approved_method = "action_open"``). Without this
        hook ``action_open()`` can be called from any state, writing
        ``open`` and running every ``post_open_action`` side effect
        (analytic account creation, project creation) unconditionally.

        Runs in the ``pre_open_check`` slot, before
        ``record.write(record._prepare_open_data())``, so raising here
        leaves ``state`` and every derived record untouched.

        Allowed source states:

        * ``confirm`` -- the approval flow: ``_action_approval``
          does not write the state itself; ``action_open`` is called
          by ``mixin_multiple_approval`` while the record is still
          ``confirm``.
        * ``done`` -- the ``pob_done_2_open`` automation
          (``data/base_automation_data.xml``) reopens a ``done`` PoB
          when ``quantity_diff`` changes back to non-zero.

        :raises UserError: when ``state`` is neither ``confirm`` nor
            ``done``.
        """
        self.ensure_one()
        if self.state not in ("confirm", "done"):
            error_message = _(
                """
Context: Open document
Database ID: %s
Problem: Document cannot be opened from its current state
Solution: Open the document only from the Confirm or Done state
"""
                % (self.id,)
            )
            raise UserError(error_message)

    @ssi_decorator.post_open_action()
    def _10_create_analytic_account(self):
        """Create or resync the PoB's own analytic account on open.

        Runs after ``action_open``. Creates a new
        ``account.analytic.account`` below
        ``source_analytic_account_id`` when the PoB does not have one
        yet; otherwise resyncs the existing one so cost/revenue stay
        traceable per obligation.
        """
        self.ensure_one()
        if self.analytic_account_id:
            self._update_analytic_account()
        else:
            AA = self.env["account.analytic.account"]
            aa = AA.create(self._prepare_analytic_account())
            self.write(
                {
                    "analytic_account_id": aa.id,
                }
            )

    def _update_analytic_account(self):
        """Resync the PoB's own analytic account with current values.

        Called by ``_10_create_analytic_account`` when the PoB already
        owns an analytic account.
        """
        self.ensure_one()
        self.analytic_account_id.write(self._prepare_update_analytic_account())

    def _prepare_update_analytic_account(self):
        """Build the values resyncing the analytic account of this PoB.

        Called by ``_update_analytic_account`` when the PoB already owns
        an analytic account.  Every key is overwritten unconditionally --
        ``parent_id`` included, since its only source of truth is
        ``source_analytic_account_id`` -- so moving the PoB to another
        contract moves its analytic account in the hierarchy as well.

        Extension point: override to resync additional fields.

        :return: dict of ``account.analytic.account`` values
        """
        self.ensure_one()
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,
            "group_id": self._get_analytic_group_id(),
            "parent_id": self._get_analytic_parent_id(),
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    def _prepare_analytic_account(self):
        """Build the values of the analytic account owned by this PoB.

        Called by ``_10_create_analytic_account`` when the PoB does not
        own an analytic account yet.  ``parent_id`` puts the new account
        directly below ``source_analytic_account_id``.

        Extension point: override to add fields to the new account.

        :return: dict of ``account.analytic.account`` values
        """
        self.ensure_one()
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,
            "group_id": self._get_analytic_group_id(),
            "parent_id": self._get_analytic_parent_id(),
            "date_start": self.date_start,
            "date_end": self.date_end,
        }

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
