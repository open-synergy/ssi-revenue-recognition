# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class PerformanceObligation(models.Model):
    """
    Adds a quality control worksheet page to the performance obligation.
    Lets QC staff record ``qc_worksheet`` results (automatic or manual)
    against a PoB before its revenue is recognised, without changing any
    of the base model's transaction states or fields.
    """

    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
        "mixin.qc_worksheet",
    ]
    _qc_worksheet_create_page = True
