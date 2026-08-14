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
    this module: the ``operating_unit_id`` field.
    """

    @classmethod
    def setUpClass(cls):
        """Grant admin the group needed to create an Acceptance."""
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: create needs `*_user_group`. `base.user_admin` is
        # already a member of `operating_unit.group_multi_operating_unit`
        # (via `group_manager_operating_unit`, granted by data, not demo)
        # and already owns `operating_unit.main_operating_unit`, so no
        # extra Operating Unit fixture is needed.
        cls.env.ref(
            "ssi_revenue_recognition.performance_obligation_acceptance_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

    def test_create(self):
        """Run the delta create tour for
        ``performance_obligation_acceptance``.

        IK: docs/performance_obligation_acceptance/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_operating_unit_performance_obligation_acceptance_create",
            login="admin",
        )
