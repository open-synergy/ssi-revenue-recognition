# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPerformanceObligation(HttpSavepointCase):
    """Tour test for the ``performance_obligation`` IK extension.

    Covers the delta of ``docs/performance_obligation/01-create.md``
    added by this module: the ``mixin.qc_worksheet`` **Quality
    Control** tab.
    """

    @classmethod
    def setUpClass(cls):
        """Grant admin the group needed to create a Performance
        Obligation.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: create needs `*_user_group`.
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

    def test_create(self):
        """Run the delta create tour for ``performance_obligation``.

        IK: docs/performance_obligation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_performance_obligation_quality_control_performance_obligation_create",
            login="admin",
        )
