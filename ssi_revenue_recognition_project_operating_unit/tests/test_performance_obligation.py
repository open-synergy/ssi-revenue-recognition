# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligation(YamlTransactionCase):
    """Scenario tests for PoB-to-project Operating Unit propagation.

    Covers the ``_prepare_project_data`` override in this glue module:
    opening a Performance Obligation (PoB) with ``auto_create_project``
    enabled must carry the PoB's own ``operating_unit_id`` -- not a
    constant, not the acting user's default -- onto the
    ``project.project`` it creates, proven for two distinct operating
    units. Also covers calling ``action_open`` directly on a ``draft``
    PoB (rejected with ``UserError``, no project created), and that a
    user without rights over the PoB's operating unit is denied read
    access to the project it produced.
    """

    def test_performance_obligation(self):
        """Run the PoB-to-project operating unit propagation scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation.yaml")
