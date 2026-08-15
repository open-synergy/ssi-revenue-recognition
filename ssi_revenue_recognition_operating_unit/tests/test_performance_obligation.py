# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligation(YamlTransactionCase):
    """Scenario tests for ``performance_obligation`` operating unit.

    Covers issue #59: ``operating_unit_id`` is stamped as a plain,
    editable field on ``performance_obligation`` -- not derived from
    the acting user's default operating unit -- and a user who is
    only granted the second operating unit's sibling group but not
    assigned to that operating unit is denied read access to a PoB
    owned by it. Also covers issue #72: once the PoB reaches
    ``done``, writing ``operating_unit_id`` is rejected with a
    ``UserError`` instead of silently going through.
    """

    def test_performance_obligation(self):
        """Run the PoB operating unit scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation.yaml")
