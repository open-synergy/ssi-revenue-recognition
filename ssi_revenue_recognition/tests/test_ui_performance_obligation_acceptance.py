# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPerformanceObligationAcceptance(HttpSavepointCase):
    """Tour tests for the ``performance_obligation_acceptance`` work
    instructions.
    """

    @classmethod
    def setUpClass(cls):
        """Create the partner, an Open PoB, and the acceptance fixtures."""
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: Confirm needs `*_user_group`; Approve/Reject/
        # Cancel/Restart/Restart Approval need `*_validator_group`.
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_acceptance_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_acceptance_validator_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        # Pre-Condition of the cancel tour: a cancel reason must exist.
        # `global_use=True` makes it selectable for every model.
        cls.env["base.cancel_reason"].create(
            {"name": "TOUR Cancel Reason", "code": "TOURCR", "global_use": True}
        )

        cls.partner = cls.env["res.partner"].create({"name": "TOUR-POBA-PARTNER"})
        # Dedicated partner for the delete fixture (see `_create` below):
        # its document number must stay "/" for `unlink()` to succeed
        # (`_check_document_number_unlink`), so it cannot be identified
        # in the list by its "# Document" text like the other fixtures.
        # This partner is the row's identifying text instead.
        cls.partner_delete = cls.env["res.partner"].create(
            {"name": "TOUR-POBA-DELETE-PARTNER"}
        )
        source_aa = cls.env["account.analytic.account"].create(
            {"name": "TOUR-POBA-SOURCE-AA", "partner_id": cls.partner.id}
        )
        # Background data: an already-Open PoB the acceptance tours pick
        # from the `# Performance Obligation` dropdown. Its own workflow is
        # not under test here, so the state is set directly instead of
        # running the full approval chain.
        cls.pob = cls.env["performance_obligation"].create(
            {
                "title": "TOUR-POBA-POB",
                "source_analytic_account_id": source_aa.id,
                "user_id": cls.admin.id,
                "name": "PB-TOUR-POBA-1",
            }
        )
        cls.pob.write({"state": "open"})

        Poa = cls.env["performance_obligation_acceptance"]

        def _create(name, partner=None):
            """Create a draft acceptance fixture with the given ``name``.

            :param name: value assigned to the document number field,
                so the tour can select the record via its display name.
                Pass ``None`` to leave it at its "/" default (required
                for a fixture that the tour will delete, since
                `unlink()` refuses any document number other than "/").
            :param partner: partner to link; defaults to
                ``cls.partner``.
            :return: the created ``performance_obligation_acceptance``
                record.
            """
            values = {
                "partner_id": (partner or cls.partner).id,
                "performance_obligation_id": cls.pob.id,
                "date": "2026-01-15",
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "user_id": cls.admin.id,
            }
            if name is not None:
                values["name"] = name
            return Poa.create(values)

        cls.poa_edit = _create("POA-TOUR-EDIT")
        # Document number stays "/" (see `_create` docstring): the delete
        # tour identifies this row by its dedicated partner instead of by
        # "# Document" text.
        cls.poa_delete = _create(None, partner=cls.partner_delete)
        cls.poa_confirm = _create("POA-TOUR-CONFIRM")
        cls.poa_approve = _create("POA-TOUR-APPROVE")
        cls.poa_approve.action_confirm()
        cls.poa_approve.invalidate_cache()
        cls.poa_reject = _create("POA-TOUR-REJECT")
        cls.poa_reject.action_confirm()
        cls.poa_reject.invalidate_cache()
        cls.poa_cancel = _create("POA-TOUR-CANCEL")
        cls.poa_restart = _create("POA-TOUR-RESTART")
        cls.poa_restart.action_cancel()
        cls.poa_restart_approval = _create("POA-TOUR-RESTARTAPPROVAL")
        cls.poa_restart_approval.action_confirm()
        cls.poa_restart_approval.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_performance_obligation_acceptance_restart_approval",
            login="admin",
        )
