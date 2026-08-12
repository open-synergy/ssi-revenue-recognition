# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PerformanceObligation(models.Model):
    """
    Adds single operating unit support to Performance Obligation.

    Unlike ``PerformanceObligationAcceptance`` and
    ``RevenueRecognition`` below, ``operating_unit_id`` here is not a
    ``related`` field and does not fall back to
    ``mixin.single_operating_unit``'s default (the acting user's
    operating unit). It is stamped at creation time by the
    ``ssi_service_revenue_recognition_operating_unit`` bridge, copied
    from the source service contract, and stays a plain, editable
    field afterwards.
    """

    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
        "mixin.single_operating_unit",
    ]

    # Operating unit is no longer derived from a service contract. It is
    # stamped at creation time by the ssi_service_revenue_recognition_operating_unit
    # bridge (from the source service contract) and stays editable otherwise.
    operating_unit_id = fields.Many2one(
        store=True,
        default=False,
    )
