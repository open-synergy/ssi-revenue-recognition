# Create Performance Obligation

> **Module:** ssi_revenue_recognition_operating_unit
>
> **Extends:** ssi_revenue_recognition — model `performance_obligation`, action
> `01-create`

## Additional Fields

When this module is installed, the form shows one more field next to **Company**:

- **Operating Unit**: The operating unit that owns this Performance Obligation. Only
  shown when the current user belongs to more than one operating unit (group
  `operating_unit.group_multi_operating_unit`). Unlike **Performance Obligation
  Acceptance** and **Revenue Recognition**, this field is a plain, stored field — it is
  stamped once at creation time by the `ssi_service_revenue_recognition_operating_unit`
  bridge module, copied from the source contract's operating unit, and has no default of
  its own on this form. This module places no read-only restriction of its own on the
  field: it stays an editable field in every status of the record — **Draft**, **Waiting
  for Approval**, **Open**, and **Done** alike.

## Modified — Record Visibility

- The Performance Obligation list is filtered by operating unit (record rule
  `performance_obligation_rule_ou`): a user only sees records whose **Operating Unit**
  is one of the operating units assigned to them. Changing the field can therefore make
  a record disappear from, or reappear in, the current user's list. This is not a Flow
  step.

## Additional Post-Condition

- Every **Performance Obligation Acceptance** and **Revenue Recognition** record linked
  to this Performance Obligation mirrors its **Operating Unit** through a stored
  `related` field. Changing **Operating Unit** here, at any time, therefore also changes
  the operating unit shown on every Acceptance and Revenue Recognition record already
  linked to it — see `docs/performance_obligation_acceptance/01-create.md` and
  `docs/revenue_recognition/01-create.md` in this module.
