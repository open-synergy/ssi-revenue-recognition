# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPerformanceObligation(HttpSavepointCase):
    """Tour tests for the ``performance_obligation`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the analytic accounts and PoB fixtures the tours need."""
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: Confirm/Cancel need `*_user_group`, Approve/Reject/
        # Restart need `*_validator_group` (the approval template's approver
        # group). Both are granted to admin so every tour's button renders.
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_validator_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        # Pre-Condition of the cancel tour: a cancel reason must exist.
        # `global_use=True` makes it selectable for every model, including
        # `performance_obligation`.
        cls.env["base.cancel_reason"].create(
            {"name": "TOUR Cancel Reason", "code": "TOURCR", "global_use": True}
        )

        AA = cls.env["account.analytic.account"]
        cls.source_aa = AA.create({"name": "TOUR-POB-SOURCE-AA"})

        Pob = cls.env["performance_obligation"]
        cls.pob_create = Pob.create(
            {
                "title": "TOUR-POB-CREATE",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_edit = Pob.create(
            {
                "title": "TOUR-POB-EDIT",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_delete = Pob.create(
            {
                "title": "TOUR-POB-DELETE",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_confirm = Pob.create(
            {
                "title": "TOUR-POB-CONFIRM",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_approve = Pob.create(
            {
                "title": "TOUR-POB-APPROVE",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_approve.action_confirm()
        cls.pob_approve.invalidate_cache()
        cls.pob_reject = Pob.create(
            {
                "title": "TOUR-POB-REJECT",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_reject.action_confirm()
        cls.pob_reject.invalidate_cache()
        cls.pob_cancel = Pob.create(
            {
                "title": "TOUR-POB-CANCEL",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_restart = Pob.create(
            {
                "title": "TOUR-POB-RESTART",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
            }
        )
        cls.pob_restart.action_cancel()

    def test_create(self):
        """Run the create tour for ``performance_obligation``.

        IK: docs/performance_obligation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``performance_obligation``.

        IK: docs/performance_obligation/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``performance_obligation``.

        IK: docs/performance_obligation/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``performance_obligation``.

        IK: docs/performance_obligation/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``performance_obligation``.

        IK: docs/performance_obligation/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``performance_obligation``.

        IK: docs/performance_obligation/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``performance_obligation``.

        IK: docs/performance_obligation/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``performance_obligation``.

        IK: docs/performance_obligation/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_restart",
            login="admin",
        )
