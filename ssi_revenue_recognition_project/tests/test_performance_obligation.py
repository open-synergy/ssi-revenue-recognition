# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligation(YamlTransactionCase):
    """Scenario tests for PoB-driven ``project.project`` provisioning.

    Covers ``_01_create_project`` (``post_open_action`` hook): opening a
    PoB with ``auto_create_project`` enabled must create a
    ``project.project`` without sending the invalid ``code`` key, and
    opening a PoB with it disabled must not create any project.
    """

    def test_performance_obligation(self):
        """Run the PoB auto-create-project scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation.yaml")
