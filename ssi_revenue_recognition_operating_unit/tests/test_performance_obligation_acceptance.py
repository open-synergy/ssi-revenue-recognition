# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligationAcceptance(YamlTransactionCase):
    """Scenario tests for ``performance_obligation_acceptance`` OU.

    Covers issue #59: ``operating_unit_id`` is a stored ``related``
    field mirroring ``performance_obligation_id.operating_unit_id``,
    so an acceptance always carries its performance obligation's
    operating unit -- proven here with an operating unit that is not
    the acting user's default one. Also covers issue #72: once the
    acceptance reaches ``done``, writing ``operating_unit_id`` is
    rejected with a ``UserError`` even though the related field is
    only readonly at the UI layer.
    """

    def test_performance_obligation_acceptance(self):
        """Run the acceptance operating unit propagation scenario."""
        self.run_yaml_scenario("test_data_performance_obligation_acceptance.yaml")
