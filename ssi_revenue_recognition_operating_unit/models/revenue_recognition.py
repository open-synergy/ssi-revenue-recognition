# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class RevenueRecognition(models.Model):
    """
    Adds single operating unit support to Revenue Recognition.

    ``operating_unit_id`` is a stored ``related`` field that mirrors
    ``performance_obligation_id.operating_unit_id``, keeping the
    performance obligation, its acceptance, and this revenue
    recognition record on the same operating unit instead of falling
    back to the acting user's default operating unit. Odoo marks
    ``related`` fields readonly by default (no explicit ``readonly=``
    anywhere in the inheritance chain), but that is a view-layer
    attribute only -- ``write()`` still tunnels straight through the
    ORM, so the field stays locked here once the document is
    ``done``; see ``write()``.
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

    def write(self, vals):
        """Reject changing ``operating_unit_id`` once ``done``.

        ``operating_unit_id`` is a stored ``related`` field, marked
        readonly for the UI only -- a direct ``write()`` (server
        action, import, RPC) still reaches ``Field.write()`` and
        succeeds regardless of that UI attribute. This guards the
        same rule as ``PerformanceObligation.write()`` at this
        model's own level, since a related write bypasses the
        parent's constraint entirely.

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
