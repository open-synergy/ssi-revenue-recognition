# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class ServiceContractPerformanceObligation(models.Model):
    _name = "service_contract.performance_obligation"
    _inherit = [
        "service_contract.performance_obligation",
    ]

    auto_create_project = fields.Boolean(
        string="Auto Create Project",
        default=False,
    )
    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )

    @api.onchange(
        "contract_id",
    )
    def onchange_auto_create_project(self):
        if self.contract_id:
            self.auto_create_project = self.contract_id.type_id.pob_auto_create_project

    @ssi_decorator.post_open_action()
    def _01_create_project(self):
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
        self.ensure_one()
        return {
            "name": self.title,
            "code": self.name,
            "analytic_account_id": self.analytic_account_id.id,
            "partner_id": self.partner_id.id,
            "date_start": self.date_start,
            "date": self.date_end,
        }
