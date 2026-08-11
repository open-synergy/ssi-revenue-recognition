# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAccountAnalyticAccount(YamlTransactionCase):
    """Scenario tests for ``account.analytic.account`` PoB Cost/Revenue.

    Covers OFS/26/000024: the core "Cost/Revenue" smart button only
    shows analytic lines posted directly to an analytic account, but
    revenue recognition journals for a contract's Performance
    Obligations post to each PoB's own, separately auto-created
    analytic account (see
    ``performance_obligation._10_create_analytic_account``) -- never
    to the source contract's own account. ``pob_cost_revenue_count``
    and ``action_open_pob_cost_revenue`` aggregate those PoB-owned
    accounts' lines so the recap is visible from the source account.
    """

    def test_account_analytic_account(self):
        """Run the PoB Cost/Revenue compute scenario."""
        self.run_yaml_scenario("test_data_account_analytic_account.yaml")

    def test_action_open_pob_cost_revenue_returns_action(self):
        """Assert the act_window dict returned by the smart button.

        Pure Python -- trigger P1 (L-01: ``action: call`` in YAML
        discards a method's return value, so the domain/res_model
        this action builds cannot be asserted from YAML at all).
        """
        source_aa = self.env["account.analytic.account"].create(
            {"name": "Test Source AA - action"}
        )
        pob_aa = self.env["account.analytic.account"].create(
            {"name": "Test PoB AA - action"}
        )
        self.env["performance_obligation"].create(
            {
                "title": "Test PoB - action",
                "source_analytic_account_id": source_aa.id,
                "analytic_account_id": pob_aa.id,
            }
        )
        action = source_aa.action_open_pob_cost_revenue()
        self.assertEqual(action["res_model"], "account.analytic.line")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["domain"], [("account_id", "in", [pob_aa.id])])
