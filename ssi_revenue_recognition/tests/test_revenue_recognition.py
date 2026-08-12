# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestRevenueRecognition(YamlTransactionCase):
    """Scenario tests for ``revenue_recognition`` security.

    Covers issue #44: moving ``security/ir.model.access.csv`` ahead of
    ``security/ir_rule/*.xml`` in ``__manifest__.py`` must not change
    the effective access rules -- a user in the ``revenue_recognition``
    group can still create a document in ``draft``, and a user outside
    that group is still rejected with ``AccessError``.
    """

    def test_revenue_recognition(self):
        """Run the create-access scenarios for ``revenue_recognition``."""
        self.run_yaml_scenario("test_data_revenue_recognition.yaml")
