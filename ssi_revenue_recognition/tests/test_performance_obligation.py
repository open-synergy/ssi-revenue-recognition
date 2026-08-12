# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligation(YamlTransactionCase):
    """Scenario tests for ``performance_obligation`` analytic parenting.

    Covers the analytic account a Performance Obligation owns: on
    ``_10_create_analytic_account`` it must end up directly below the
    contract's ``source_analytic_account_id`` in the
    ``account.analytic.account`` hierarchy, on both the create and the
    update path, and it must stay a root when the source account is the
    PoB's own analytic account (OCA ``account_analytic_parent`` forbids
    recursive hierarchies).
    """

    def test_performance_obligation(self):
        """Run the PoB analytic account parenting scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation.yaml")
