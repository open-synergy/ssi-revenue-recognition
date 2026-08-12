# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class PerformanceObligation(models.Model):
    """
    Adds optional ``project.project`` provisioning to Performance
    Obligation (PoB).
    When ``auto_create_project`` is enabled, opening the PoB creates
    (or refreshes) a linked project so delivery work for that PoB can
    be tracked in the Project app, without requiring a manual project
    to be created and linked by hand.
    """

    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
    ]

    auto_create_project = fields.Boolean(
        string="Auto Create Project",
        default=False,
    )
    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )

    @ssi_decorator.post_open_action()
    def _01_create_project(self):
        """Provision the delivery project when the PoB is opened.

        Runs after the Performance Obligation transitions to the
        ``open`` state (``post_open_action`` hook). Does nothing when
        ``auto_create_project`` is disabled.

        Side effect: creates a ``project.project`` record from
        ``_prepare_project_data`` and links it through ``project_id``
        when the PoB has none yet; when a project is already linked,
        that project is updated in place with the same values instead
        of creating a duplicate.
        """
        self.ensure_one()
        Project = self.env["project.project"]

        if not self.auto_create_project:
            return True

        if not self.project_id:
            project = Project.create(self._prepare_project_data())
            self.write({"project_id": project.id})
        else:
            self.project_id.write(self._prepare_project_data())

    def _prepare_project_data(self):
        """Build the ``project.project`` values for this PoB.

        Extension point: override in a derived module to add or
        change fields (e.g. ``..._project_operating_unit`` overrides
        this to propagate the operating unit) without touching
        ``_01_create_project``.

        :return: dict of ``project.project`` values (``name``,
            ``code``, ``analytic_account_id``, ``partner_id``,
            ``date_start``, ``date``)
        """
        self.ensure_one()
        return {
            "name": self.title,
            "code": self.name,
            "analytic_account_id": self.analytic_account_id.id,
            "partner_id": self.partner_id.id,
            "date_start": self.date_start,
            "date": self.date_end,
        }
