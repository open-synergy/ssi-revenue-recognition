# Create Performance Obligation Acceptance

> **Module:** ssi_revenue_recognition_work_log
>
> **Extends:** ssi_revenue_recognition — model `performance_obligation_acceptance`,
> action `01-create`

## Modified Flow

- Anchor: visible on the form from the moment it opens (before step 3 of the base Flow),
  and present in every status afterward — two tabs are added by this module.

- **Work Log** tab (`mixin.work_object`) — the same tab this module adds to
  **Performance Obligation** and **Revenue Recognition**; see
  `docs/performance_obligation/01-create.md` in this module. It holds an editable **Work
  Log Analytic Account**, an editable **Estimation**, an editable **Work Logs** list
  (`hr.work_log` lines linked to this Acceptance), and read-only
  **Total**/**Remaining**/**Excess** figures kept in sync with that list against
  **Estimation**.

- **Fullfilment Work Logs** tab — this tab is specific to Acceptance:
  - It shows an editable **Work Logs** list, but the work logs offered for selection are
    restricted to the set computed in `allowed_work_log_ids`: only `hr.work_log` records
    booked against the linked Performance Obligation's analytic account, dated within
    this Acceptance's **Date Start**/**Date End** window, and in status **Done**, can be
    picked here.
  - Selecting or removing lines automatically updates **Work Qty**, a read-only field on
    the same tab, to reflect the lines currently selected. This module does not document
    how the figure is derived — see the model's docstring for that detail.
