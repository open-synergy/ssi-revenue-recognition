# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase does not set
# up cls.env in setUpClass, so the Pre-Condition fixture below would
# fail with AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPerformanceObligation(HttpSavepointCase):
    """Tour tests for the ``performance_obligation`` auto project delta."""

    @classmethod
    def setUpClass(cls):
        """Create a PoB pending approval, with Auto Create Project on.

        Pre-Condition of the approve delta tour: the record must be in
        the ``confirm`` state (Waiting for Approval) and the ``admin``
        user (who runs the tour) must be a registered approver --
        both requirements inherited from the base module's own
        ``05-approve.md`` Pre-Condition. ``auto_create_project`` is set
        so the delta's side effect (docs/performance_obligation/
        05-approve.md) actually runs once the record is approved.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_validator_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        AA = cls.env["account.analytic.account"]
        cls.source_aa = AA.create({"name": "TOUR-POB-PROJECT-SOURCE-AA"})

        Pob = cls.env["performance_obligation"]
        cls.pob_approve = Pob.create(
            {
                "title": "TOUR-POB-PROJECT-APPROVE",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
                "auto_create_project": True,
            }
        )
        cls.pob_approve.action_confirm()
        cls.pob_approve.invalidate_cache()

    def test_approve_creates_project(self):
        """Run the approve delta tour for ``performance_obligation``.

        IK: docs/performance_obligation/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_project_performance_obligation_approve",
            login="admin",
        )
