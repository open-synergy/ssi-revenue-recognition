# Create Performance Obligation

> **Module:** ssi_revenue_recognition_work_log
>
> **Extends:** ssi_revenue_recognition — model `performance_obligation`, action
> `01-create`

## Modified Flow

- Anchor: visible on the form from the moment it opens (before step 3 of the base Flow),
  and present in every status afterward — a **Work Log** tab is added by this module
  (`mixin.work_object`). It holds:
  - **Work Log Analytic Account**: an editable field to pick the analytic account work
    logs on this PoB are expected to be booked against. Optional, no default.
  - **Estimation**: an editable hour figure for the work planned on this PoB.
  - An editable **Work Logs** list — `hr.work_log` lines linked to this PoB. Lines can
    be added, edited, and removed directly on this tab, in any status.
  - Read-only **Total**, **Remaining**, and **Excess** figures, kept in sync with the
    **Work Logs** list against **Estimation**. This module does not document how the
    figures are derived — see the model's docstring for that detail.
