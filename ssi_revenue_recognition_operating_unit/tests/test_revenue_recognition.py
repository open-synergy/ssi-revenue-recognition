# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestRevenueRecognition(YamlTransactionCase):
    """Scenario tests for ``revenue_recognition`` operating unit.

    Covers issue #59: ``operating_unit_id`` is a stored ``related``
    field mirroring ``performance_obligation_id.operating_unit_id``,
    so a revenue recognition always carries its performance
    obligation's operating unit -- proven here with an operating unit
    that is not the acting user's default one.
    """

    def test_revenue_recognition(self):
        """Run the revenue recognition operating unit propagation scenario."""
        self.run_yaml_scenario("test_data_revenue_recognition.yaml")
