# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestAccountAnalyticAccount(YamlTransactionCase):
    """Covers OFS/26/000024's revision to the core "Cost/Revenue" button.

    The core button only showed analytic lines posted directly to the
    opened analytic account. A Performance Obligation's revenue
    recognition journals post to its own, separately auto-created
    analytic account (see
    ``performance_obligation._10_create_analytic_account``), which
    ``account_analytic_parent`` places as a child of the source
    contract's account
    (``performance_obligation._get_analytic_parent_id``) -- so the
    button never showed them.
    ``analytic.account_analytic_line_action`` is overridden here to
    browse the whole child subtree instead of an exact match.
    """

    def test_cost_revenue_action_domain_includes_child_accounts(self):
        """Assert the overridden action's domain reaches child accounts.

        Pure Python -- trigger P1 (L-02: the actual side of a YAML
        ``assert`` is always a dotted ``getattr`` on a registry record;
        it cannot evaluate a field's string content as a domain
        expression against a resolved ``active_id`` and search with
        it).
        """
        parent_aa = self.env["account.analytic.account"].create(
            {"name": "Test Parent AA - child_of"}
        )
        child_aa = self.env["account.analytic.account"].create(
            {"name": "Test Child AA - child_of", "parent_id": parent_aa.id}
        )
        child_line = self.env["account.analytic.line"].create(
            {"name": "Test child line", "account_id": child_aa.id, "amount": 1000.0}
        )
        other_aa = self.env["account.analytic.account"].create(
            {"name": "Test Unrelated AA - child_of"}
        )
        other_line = self.env["account.analytic.line"].create(
            {"name": "Test unrelated line", "account_id": other_aa.id, "amount": 1.0}
        )

        action = self.env.ref("analytic.account_analytic_line_action")
        domain = safe_eval(action.domain, {"active_id": parent_aa.id})
        lines = self.env["account.analytic.line"].search(domain)

        self.assertIn(child_line, lines)
        self.assertNotIn(other_line, lines)
