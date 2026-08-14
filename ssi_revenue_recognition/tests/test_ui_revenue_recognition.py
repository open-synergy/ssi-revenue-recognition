# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiRevenueRecognition(HttpSavepointCase):
    """Tour tests for the ``revenue_recognition`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the type, an Open PoB with a Done acceptance, and RR
        fixtures.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: Confirm needs `*_user_group`; Approve/Reject/
        # Cancel/Restart/Restart Approval need `*_validator_group`.
        cls.env.ref(
            "ssi_revenue_recognition.revenue_recognition_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})
        cls.env.ref(
            "ssi_revenue_recognition.revenue_recognition_validator_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        # Pre-Condition of the cancel tour: a cancel reason must exist.
        # `global_use=True` makes it selectable for every model.
        cls.env["base.cancel_reason"].create(
            {"name": "TOUR Cancel Reason", "code": "TOURCR", "global_use": True}
        )

        cls.partner = cls.env["res.partner"].create({"name": "TOUR-RR-PARTNER"})
        source_aa = cls.env["account.analytic.account"].create(
            {"name": "TOUR-RR-SOURCE-AA", "partner_id": cls.partner.id}
        )
        # Background data: an Open PoB with a Done acceptance, so the
        # `# Performance Obligation` dropdown and the `Populate` action have
        # something to work with. Neither model's own workflow is under
        # test here, so their state is set directly.
        cls.pob = cls.env["performance_obligation"].create(
            {
                "title": "TOUR-RR-POB",
                "source_analytic_account_id": source_aa.id,
                "user_id": cls.admin.id,
                "name": "PB-TOUR-RR-1",
            }
        )
        cls.pob.write({"state": "open"})
        cls.poa = cls.env["performance_obligation_acceptance"].create(
            {
                "name": "POA-TOUR-RR-1",
                "partner_id": cls.partner.id,
                "performance_obligation_id": cls.pob.id,
                "date": "2026-01-15",
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "user_id": cls.admin.id,
            }
        )
        cls.poa.write({"state": "done"})

        journal = cls.env["account.journal"].create(
            {"name": "TOUR RR Journal", "code": "TOURRRJ", "type": "general"}
        )
        usage = cls.env["product.usage_type"].create(
            {"name": "TOUR RR Usage", "code": "TOURRRUS"}
        )
        cls.rr_type = cls.env["revenue_recognition_type"].create(
            {
                "name": "TOUR-RR-TYPE",
                "code": "TOURRRTYPE",
                "journal_id": journal.id,
                "unearned_income_usage_id": usage.id,
                "income_usage_id": usage.id,
            }
        )
        unearned_account = cls.env["account.account"].create(
            {
                "name": "TOUR RR Unearned Income Account",
                "code": "TOURRRUA",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_current_liabilities"
                ).id,
            }
        )
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR RR Income Account",
                "code": "TOURRRIA",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )

        Rr = cls.env["revenue_recognition"]

        def _create(name):
            """Create a draft RR fixture with the given ``name``, populated.

            :param name: value assigned to the document number field,
                so the tour can select the record via its display name.
            :return: the created ``revenue_recognition`` record, after
                running the same population steps as the ``Populate``
                button.
            """
            record = Rr.create(
                {
                    "name": name,
                    "type_id": cls.rr_type.id,
                    "journal_id": journal.id,
                    "partner_id": cls.partner.id,
                    "performance_obligation_id": cls.pob.id,
                    "unearned_income_account_id": unearned_account.id,
                    "income_account_id": income_account.id,
                    "date": "2026-01-31",
                    "date_start": "2026-01-01",
                    "date_end": "2026-01-31",
                    "user_id": cls.admin.id,
                }
            )
            record._populate_pob_acceptances()
            record._populate_wip_move_line()
            return record

        cls.rr_edit = _create("RR-TOUR-EDIT")
        cls.rr_delete = _create("RR-TOUR-DELETE")
        cls.rr_confirm = _create("RR-TOUR-CONFIRM")
        cls.rr_approve = _create("RR-TOUR-APPROVE")
        cls.rr_approve.action_confirm()
        cls.rr_approve.invalidate_cache()
        cls.rr_reject = _create("RR-TOUR-REJECT")
        cls.rr_reject.action_confirm()
        cls.rr_reject.invalidate_cache()
        cls.rr_cancel = _create("RR-TOUR-CANCEL")
        cls.rr_restart = _create("RR-TOUR-RESTART")
        cls.rr_restart.action_cancel()
        cls.rr_restart_approval = _create("RR-TOUR-RESTARTAPPROVAL")
        cls.rr_restart_approval.action_confirm()
        cls.rr_restart_approval.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_restart_approval",
            login="admin",
        )
