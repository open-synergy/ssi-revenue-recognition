# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PerformanceObligationAcceptance(models.Model):
    """
    Adds single operating unit support to Performance Obligation
    Acceptance.

    ``operating_unit_id`` is a stored ``related`` field that mirrors
    ``performance_obligation_id.operating_unit_id``, so an acceptance
    always carries its performance obligation's operating unit
    instead of falling back to the acting user's default operating
    unit.
    """

    _name = "performance_obligation_acceptance"
    _inherit = [
        "performance_obligation_acceptance",
        "mixin.single_operating_unit",
    ]

    # Acceptance inherits its operating unit from its performance obligation
    # (which is itself analytic-account based), instead of from a service contract.
    operating_unit_id = fields.Many2one(
        related="performance_obligation_id.operating_unit_id",
        store=True,
        default=False,
    )
