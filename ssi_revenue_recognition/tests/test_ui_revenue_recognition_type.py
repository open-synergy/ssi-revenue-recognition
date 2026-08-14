# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase, lihat structure-and-runner.md §Base class.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiRevenueRecognitionType(HttpSavepointCase):
    """Tour tests for the ``revenue_recognition_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and create the type fixtures."""
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: this master data menu is gated by the configurator
        # group. Without it the tour dies on its FIRST step — the menu is
        # never rendered.
        cls.env.ref(
            "ssi_revenue_recognition.revenue_recognition_type_configuration_group"
        ).sudo().write({"users": [(4, cls.admin.id)]})

        # m2o dropdown data picked by the create tour, per the identifier
        # in each step's `run: "text ..."` / `:contains(...)`.
        cls.env["account.journal"].create(
            {
                "name": "TOUR RRT Journal",
                "code": "TOURRRTJ",
                "type": "general",
            }
        )
        cls.env["product.usage_type"].create(
            {
                "name": "TOUR RRT Unearned Usage",
                "code": "TOURRRTU",
            }
        )
        cls.env["product.usage_type"].create(
            {
                "name": "TOUR RRT Income Usage",
                "code": "TOURRRTI",
            }
        )

        Type = cls.env["revenue_recognition_type"]
        journal = cls.env["account.journal"].search([("type", "=", "general")], limit=1)
        usage = cls.env["product.usage_type"].search([], limit=1)
        cls.rrt_edit = Type.create(
            {
                "name": "TOUR-RRT-EDIT",
                "code": "TOURRRTEDIT",
                "journal_id": journal.id,
                "unearned_income_usage_id": usage.id,
                "income_usage_id": usage.id,
            }
        )
        cls.rrt_delete = Type.create(
            {
                "name": "TOUR-RRT-DELETE",
                "code": "TOURRRTDEL",
                "journal_id": journal.id,
                "unearned_income_usage_id": usage.id,
                "income_usage_id": usage.id,
            }
        )
        cls.rrt_deactivate = Type.create(
            {
                "name": "TOUR-RRT-DEACTIVATE",
                "code": "TOURRRTDEACT",
                "journal_id": journal.id,
                "unearned_income_usage_id": usage.id,
                "income_usage_id": usage.id,
            }
        )
        cls.rrt_activate = Type.create(
            {
                "name": "TOUR-RRT-ACTIVATE",
                "code": "TOURRRTACT",
                "journal_id": journal.id,
                "unearned_income_usage_id": usage.id,
                "income_usage_id": usage.id,
            }
        )
        # Pre-Condition of the activate tour: the record starts archived.
        cls.rrt_activate.write({"active": False})

    def test_create(self):
        """Run the create tour for ``revenue_recognition_type``.

        IK: docs/revenue_recognition_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_type_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``revenue_recognition_type``.

        IK: docs/revenue_recognition_type/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_type_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``revenue_recognition_type``.

        IK: docs/revenue_recognition_type/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_type_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``revenue_recognition_type``.

        IK: docs/revenue_recognition_type/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_type_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``revenue_recognition_type``.

        IK: docs/revenue_recognition_type/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_revenue_recognition_revenue_recognition_type_activate",
            login="admin",
        )
