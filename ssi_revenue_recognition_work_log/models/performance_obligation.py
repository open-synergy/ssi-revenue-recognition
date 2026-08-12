# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class PerformanceObligation(models.Model):
    """
    Adds work log tracking to the Performance Obligation (PoB) via
    ``mixin.work_object``. Enables the ``hr.work_log`` tab on the
    PoB form (``_work_log_create_page``) so hours logged against it
    can be compared to ``work_estimation`` and rolled up into the
    mixin's realization figures.
    """

    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
        "mixin.work_object",
    ]

    _work_log_create_page = True
