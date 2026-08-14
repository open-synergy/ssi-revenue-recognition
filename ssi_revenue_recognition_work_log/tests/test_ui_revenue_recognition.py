# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiRevenueRecognition(HttpSavepointCase):
    """Tour test for the ``revenue_recognition`` IK extension.

    Covers the delta of ``docs/revenue_recognition/01-create.md`` added
    by this module: the ``mixin.work_object`` **Work Log** tab.
    """

    @classmethod
    def setUpClass(cls):
        """Grant admin the group needed to create a Revenue
        Recognition.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: create needs `*_user_group`.
        cls.env.ref(
            "ssi_revenue_recognition.revenue_recognition_user_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

    def test_create(self):
        """Run the delta create tour for ``revenue_recognition``.

        IK: docs/revenue_recognition/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_work_log_revenue_recognition_create",
            login="admin",
        )
