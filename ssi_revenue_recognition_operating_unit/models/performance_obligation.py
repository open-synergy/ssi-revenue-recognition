# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


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
    field until the document reaches ``done`` -- see ``write()``.
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

    def write(self, vals):
        """Reject changing ``operating_unit_id`` once ``done``.

        Operating unit is stamped once at creation time and must not
        move after the performance obligation reaches ``done`` -- the
        ownership it implies (record rules, analytic reporting) would
        otherwise change silently underneath a completed document.

        :param vals: values to write, as passed to ``write()``.
        :raises UserError: when ``vals`` includes
            ``operating_unit_id`` and at least one record in ``self``
            is already in ``done`` state.
        :return: result of ``super().write()``.
        """
        if "operating_unit_id" in vals:
            for record in self.filtered(lambda r: r.state == "done"):
                error_message = _(
                    """
Context: Change operating unit
Database ID: %s
Problem: Operating unit cannot be changed once the document is done
Solution: Restart the document (action_restart) before changing its
operating unit
"""
                    % (record.id,)
                )
                raise UserError(error_message)
        return super().write(vals)
