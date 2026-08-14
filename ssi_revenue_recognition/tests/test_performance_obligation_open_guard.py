# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligationOpenGuard(YamlTransactionCase):
    """Scenario tests for the ``action_open`` source-state guard.

    Covers issue #74: ``_10_check_open_source_state`` must reject
    ``action_open`` from any state other than ``confirm`` (the
    approval flow) or ``done`` (the ``pob_done_2_open`` automation),
    while leaving both of those two flows working end to end.
    """

    def test_performance_obligation_open_guard(self):
        """Run the open source-state guard scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation_open_guard.yaml")
