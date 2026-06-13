# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PerformanceObligation(models.Model):
    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
    ]

    def _prepare_project_data(self):
        self.ensure_one()
        _super = super()
        result = _super._prepare_project_data()
        result.update(
            {
                "operating_unit_id": self.operating_unit_id
                and self.operating_unit_id.id
                or False,
            }
        )
        return result
