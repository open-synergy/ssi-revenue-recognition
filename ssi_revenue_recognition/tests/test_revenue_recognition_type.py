# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestRevenueRecognitionType(YamlTransactionCase):
    """Scenario tests for ``revenue_recognition_type`` account mapping.

    Covers issue #44: the inline ``<form>`` added to the ``account_ids``
    one2many (see ``views/revenue_recognition_type_views.xml``) must not
    change how the lines are persisted -- creating a type with two
    inline ``account_ids`` lines still saves each line's own
    ``wip_account_id``/``expense_account_id`` mapping unchanged.
    """

    def test_revenue_recognition_type(self):
        """Run the inline account_ids creation scenario."""
        self.run_yaml_scenario("test_data_revenue_recognition_type.yaml")
