# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PerformanceObligation(models.Model):
    """
    Bridges Performance Obligation (PoB), Project, and Operating Unit.
    Glues ``ssi_revenue_recognition_project`` (project provisioning),
    ``ssi_revenue_recognition_operating_unit`` (OU on the PoB), and
    ``ssi_project_operating_unit`` (OU on ``project.project``) so the
    OU on a PoB propagates to the project it auto-creates.
    """

    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
    ]

    def _prepare_project_data(self):
        """Add ``operating_unit_id`` to the project values.

        Override that calls ``super()`` and then inserts the PoB's
        ``operating_unit_id`` into the values, so the project created
        (or updated) from this PoB carries the same Operating Unit.

        :return: dict of ``project.project`` values, extended with
            ``operating_unit_id``
        """
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
