# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPerformanceObligationAcceptance(HttpSavepointCase):
    """Tour test for the ``performance_obligation_acceptance`` IK
    extension.

    Covers the delta of
    ``docs/performance_obligation_acceptance/01-create.md`` added by
    this module: the shared **Work Log** tab and the acceptance-only
    **Fullfilment Work Logs** tab (``allowed_work_log_ids`` /
    ``poa_work_log_ids`` / ``qty_work_log``).
    """

    @classmethod
    def setUpClass(cls):
        """Create the PoB, an Open timesheet, and a Done work log the
        tour can pick.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: create needs `*_user_group`.
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_acceptance_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        cls.partner = cls.env["res.partner"].create({"name": "TOUR-POBAWL-PARTNER"})
        source_aa = cls.env["account.analytic.account"].create(
            {"name": "TOUR-POBAWL-SOURCE-AA", "partner_id": cls.partner.id}
        )
        pob_aa = cls.env["account.analytic.account"].create(
            {"name": "TOUR-POBAWL-POB-AA", "partner_id": cls.partner.id}
        )
        # Background data: an already-Open PoB, on its own analytic
        # account, the tour picks from the `# Performance Obligation`
        # dropdown. Its own workflow is not under test here, so the
        # state and analytic account are set directly instead of
        # running the full approval chain (same approach as the YAML
        # scenarios in test_data_performance_obligation_acceptance.yaml).
        cls.pob = cls.env["performance_obligation"].create(
            {
                "title": "TOUR-POBAWL-POB",
                "source_analytic_account_id": source_aa.id,
                "analytic_account_id": pob_aa.id,
                "user_id": cls.admin.id,
                "name": "PB-TOUR-POBAWL-1",
            }
        )
        cls.pob.write({"state": "open"})

        # Background data: an Open `hr.timesheet` covering the work log's
        # date, so the work log passes `_check_sheet_id`
        # (`ssi_work_log_mixin`'s `_compute_sheet_id` only finds a sheet
        # when one exists for the same employee with a date range that
        # covers the log's date and status Open) — same prerequisite the
        # YAML scenarios in
        # test_data_performance_obligation_acceptance.yaml set up before
        # creating a work log.
        employee = cls.env["hr.employee"].create({"name": "TOUR-POBAWL-EMPLOYEE"})
        timesheet = cls.env["hr.timesheet"].create(
            {
                "employee_id": employee.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
            }
        )
        timesheet.action_open()

        # Background data: one Done work log booked against the PoB's
        # analytic account, dated inside the window the tour will type
        # into Date Start/Date End (2026-01-01..2026-01-31), so
        # `allowed_work_log_ids` has exactly this one candidate to
        # offer when the tour opens the Fullfilment Work Logs tab.
        ir_model = cls.env["ir.model"].search([("model", "=", "res.partner")], limit=1)
        work_log = cls.env["hr.work_log"].create(
            {
                "employee_id": employee.id,
                "description": "TOUR-POBAWL-WORKLOG-1",
                "model_id": ir_model.id,
                "work_object_id": cls.partner.id,
                "date": "2026-01-15",
                "amount": 4.0,
                "analytic_account_id": pob_aa.id,
            }
        )
        work_log.with_context(bypass_policy_check=True).action_confirm()
        work_log.with_context(bypass_policy_check=True).action_approve_approval()

    def test_create(self):
        """Run the delta create tour for
        ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_work_log_performance_obligation_acceptance_create",
            login="admin",
        )
