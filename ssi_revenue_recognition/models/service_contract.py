# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = ["service.contract"]

    analytic_budget_id = fields.Many2one(
        string="# Analytic Budget",
        comodel_name="analytic_budget.budget",
    )
    lock_budget = fields.Boolean(
        string="Lock Budget",
        default=False,
        readonly=True,
    )

    @api.onchange(
        "analytic_account_id",
    )
    def onchange_analytic_budget_id(self):
        self.analytic_budget_id = False

    def action_lock_budget(self):
        for record in self.sudo():
            record._lock_budget()

    def action_unlock_budget(self):
        for record in self.sudo():
            record._unlock_budget()

    def _lock_budget(self):
        self.ensure_one()
        self.write(
            {
                "lock_budget": True,
            }
        )

    def _unlock_budget(self):
        self.ensure_one()
        self.write(
            {
                "lock_budget": False,
            }
        )
