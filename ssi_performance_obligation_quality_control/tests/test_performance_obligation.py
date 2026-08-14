# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPerformanceObligation(YamlTransactionCase):
    """Scenario tests for ``mixin.qc_worksheet`` on ``performance_obligation``.

    Covers issue #63: the QC worksheet surface the mixin contributes
    (``qc_worksheet_ids``, ``qc_worksheet_set_id``) must be readable
    and empty on a freshly created PoB, the ``draft -> open`` approval
    flow must keep working with the mixin installed, and the existing
    ``action_open`` source-state guard must still reject a draft PoB.
    """

    def test_performance_obligation(self):
        """Run the QC worksheet surface and open-guard scenarios."""
        self.run_yaml_scenario("test_data_performance_obligation.yaml")
