# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligationAcceptance(YamlTransactionCase):
    """Scenario tests for the work log bridge on the acceptance model.

    Covers ``_compute_allowed_work_log_ids`` (the curated selection of
    ``hr.work_log`` candidates) and ``_compute_qty_work_log`` (the
    quantity summed from the logs actually picked).
    """

    def test_performance_obligation_acceptance(self):
        """Run the work log bridge scenarios for the acceptance model."""
        self.run_yaml_scenario("test_data_performance_obligation_acceptance.yaml")
