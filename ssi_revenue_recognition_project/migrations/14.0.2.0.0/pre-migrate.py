# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Pre-migration for ssi_revenue_recognition_project 14.0.2.0.0.

    The service.type field ``pob_auto_create_project`` and the service.type
    view are moved out of this module into the new bridge
    ssi_service_revenue_recognition_project. Reassign the field's ir.model.data
    ownership to the bridge BEFORE reflection so the stored column is not
    dropped by the orphan cleanup, and delete the stale view (the bridge
    recreates it on install).
    """
    _logger.info("14.0.2.0.0 (ssi_revenue_recognition_project) pre-migrate: start")

    # 1. Hand off the service.type field ownership to the project bridge.
    openupgrade.logged_query(
        cr,
        """
        UPDATE ir_model_data
        SET module = 'ssi_service_revenue_recognition_project'
        WHERE module = 'ssi_revenue_recognition_project'
          AND model = 'ir.model.fields'
          AND name = 'field_service_type__pob_auto_create_project'
        """,
    )

    # 2. Delete the stale service.type view owned by this module (recursively).
    cr.execute(
        """
        SELECT v.id
        FROM ir_ui_view v
        JOIN ir_model_data d ON d.res_id = v.id AND d.model = 'ir.ui.view'
        WHERE d.module = 'ssi_revenue_recognition_project'
          AND v.model = 'service.type'
        """
    )
    stale_ids = [r[0] for r in cr.fetchall()]
    if stale_ids:
        cr.execute(
            """
            WITH RECURSIVE desc_views AS (
                SELECT id FROM ir_ui_view WHERE id = ANY(%s)
                UNION ALL
                SELECT v.id FROM ir_ui_view v
                JOIN desc_views d ON v.inherit_id = d.id
            )
            SELECT id FROM desc_views
            """,
            (stale_ids,),
        )
        all_ids = [r[0] for r in cr.fetchall()]
        if all_ids:
            openupgrade.logged_query(
                cr,
                "DELETE FROM ir_model_data "
                "WHERE model = 'ir.ui.view' AND res_id = ANY(%s)",
                (all_ids,),
            )
            openupgrade.logged_query(
                cr,
                """
                WITH RECURSIVE desc_views AS (
                    SELECT id FROM ir_ui_view WHERE id = ANY(%s)
                    UNION ALL
                    SELECT v.id FROM ir_ui_view v
                    JOIN desc_views d ON v.inherit_id = d.id
                )
                DELETE FROM ir_ui_view WHERE id IN (SELECT id FROM desc_views)
                """,
                (stale_ids,),
            )

    _logger.info("14.0.2.0.0 (ssi_revenue_recognition_project) pre-migrate: done")
