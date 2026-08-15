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
    opening a PoB with it disabled must not create any project. Also
    asserts ``project_id`` stays empty through ``draft`` and ``confirm``
    (proving the project is born on the ``open`` transition, not
    earlier), that ``project.project`` search-resolves to exactly the
    linked record named per ``_prepare_project_data``, and that calling
    ``action_open`` directly on a ``draft`` PoB is rejected with a
    ``UserError`` (the ``_10_check_open_source_state`` guard from
    ``ssi_revenue_recognition``) without creating a project.
    """

    def test_performance_obligation(self):
        """Run the PoB auto-create-project scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation.yaml")
