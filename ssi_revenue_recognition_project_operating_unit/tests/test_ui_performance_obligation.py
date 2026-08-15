# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. 14.0's plain HttpCase does not set
# up cls.env in setUpClass, so the Pre-Condition fixture below would
# fail with AttributeError before the browser even starts (see the UI
# test skill's structure-and-runner.md, Base class section).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPerformanceObligation(HttpSavepointCase):
    """Tour test for the ``performance_obligation`` IK extension.

    Covers the delta of ``docs/performance_obligation/05-approve.md``
    added by this module: the Approve Flow still completes and reaches
    ``open`` for a PoB owned by an Operating Unit. The propagated
    Operating Unit value on the created project is unit test territory
    (``tests/test_data_performance_obligation.yaml``), not this tour's.
    """

    @classmethod
    def setUpClass(cls):
        """Create a PoB pending approval, owned by the main operating unit.

        Pre-Condition of the approve delta tour: the record must be in
        the ``confirm`` state (Waiting for Approval), and its
        ``operating_unit_id`` must be one the ``admin`` user (who runs
        the tour) is assigned to -- otherwise the record rule added by
        ``ssi_revenue_recognition_operating_unit``
        (``performance_obligation_rule_ou``) would hide it from the
        list, and the tour could never find it to open. ``admin`` is
        granted the base module's approver group and already owns
        ``operating_unit.main_operating_unit``.
        ``auto_create_project`` is set so this module's own side
        effect (project creation, whose Operating Unit follows the
        PoB) actually runs once the record is approved.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_validator_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})
        cls.main_ou = cls.env.ref("operating_unit.main_operating_unit")

        AA = cls.env["account.analytic.account"]
        cls.source_aa = AA.create({"name": "TOUR-POB-PROJECT-OU-SOURCE-AA"})

        Pob = cls.env["performance_obligation"]
        cls.pob_approve = Pob.create(
            {
                "title": "TOUR-POB-PROJECT-OU-APPROVE",
                "source_analytic_account_id": cls.source_aa.id,
                "user_id": cls.admin.id,
                "operating_unit_id": cls.main_ou.id,
                "auto_create_project": True,
            }
        )
        cls.pob_approve.action_confirm()
        cls.pob_approve.invalidate_cache()

    def test_approve_reaches_open(self):
        """Run the approve delta tour for ``performance_obligation``.

        IK: docs/performance_obligation/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_project_operating_unit_"
            "performance_obligation_approve",
            login="admin",
        )
