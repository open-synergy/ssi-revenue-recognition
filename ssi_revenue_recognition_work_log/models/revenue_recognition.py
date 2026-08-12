# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import models


class RevenueRecognition(models.Model):
    """
    Adds work log tracking to Revenue Recognition via
    ``mixin.work_object``. Enables the ``hr.work_log`` tab on the
    form (``_work_log_create_page``) so hours logged while performing
    the recognition can be compared to ``work_estimation`` and rolled
    up into the mixin's realization figures.
    """

    _name = "revenue_recognition"
    _inherit = [
        "revenue_recognition",
        "mixin.work_object",
    ]

    _work_log_create_page = True
