# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class PerformanceObligationAcceptance(models.Model):
    _name = "performance_obligation_acceptance"
    _inherit = [
        "performance_obligation_acceptance",
    ]

    allowed_work_log_ids = fields.Many2many(
        string="Allowed Work Logs",
        comodel_name="hr.work_log",
        compute="_compute_allowed_work_log_ids",
        store=False,
    )
    work_log_ids = fields.Many2many(
        string="Work Logs",
        comodel_name="hr.work_log",
        relation="rel_poa_2_work_log",
        column1="poa_id",
        column2="work_log_id",
    )
    qty_work_log = fields.Float(
        string="Work Qty",
        compute="_compute_qty_work_log",
        store=True,
    )

    @api.depends(
        "date_start",
        "date_end",
        "performance_obligation_id",
    )
    def _compute_allowed_work_log_ids(self):
        for record in self:
            pob = record.performance_obligation_id

            WorkLog = self.env["hr.work_log"]
            criteria = [
                ("analytic_account_id", "=", pob.analytic_account_id.id),
                ("date", ">=", record.date_start),
                ("date", "<=", record.date_end),
                ("state", "=", "done"),
            ]
            record.allowed_work_log_ids = WorkLog.search(criteria).ids

    @api.depends(
        "work_log_ids",
        "work_log_ids.quantity",
    )
    def _compute_qty_work_log(self):
        for record in self:
            result = 0.0
            for work_log in record.work_log_ids:
                result += work_log.quantity
            record.qty_work_log = result
            record._compute_qty_fulfilled()
