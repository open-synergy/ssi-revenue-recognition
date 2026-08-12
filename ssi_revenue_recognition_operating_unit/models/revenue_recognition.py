# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RevenueRecognition(models.Model):
    """
    Adds single operating unit support to Revenue Recognition.

    ``operating_unit_id`` is a stored ``related`` field that mirrors
    ``performance_obligation_id.operating_unit_id``, keeping the
    performance obligation, its acceptance, and this revenue
    recognition record on the same operating unit instead of falling
    back to the acting user's default operating unit.
    """

    _name = "revenue_recognition"
    _inherit = [
        "revenue_recognition",
        "mixin.single_operating_unit",
    ]

    # Revenue recognition inherits its operating unit from its performance
    # obligation, so performance obligation, acceptance, and revenue recognition
    # always share the same operating unit.
    operating_unit_id = fields.Many2one(
        related="performance_obligation_id.operating_unit_id",
        store=True,
        default=False,
    )
