# Create Performance Obligation Acceptance

> **Module:** ssi_revenue_recognition_operating_unit
>
> **Extends:** ssi_revenue_recognition — model `performance_obligation_acceptance`,
> action `01-create`

## Additional Fields

When this module is installed, the form shows one more field next to **Company**:

- **Operating Unit**: The operating unit that owns this Acceptance. Only shown when the
  current user belongs to more than one operating unit (group
  `operating_unit.group_multi_operating_unit`). It is a stored `related` field that
  mirrors **Performance Obligation > Operating Unit**, so a new Acceptance always
  carries its Performance Obligation's operating unit instead of falling back to the
  acting user's own default operating unit. This module places no read-only restriction
  of its own on the field: it stays an editable field in every status of the record —
  **Draft**, **Waiting for Approval**, and **Done** alike. Because the field it mirrors
  is not itself read-only, this field keeps an active inverse — see
  `## Additional Post-Condition` below for what changing it here actually does.

## Modified — Record Visibility

- The Performance Obligation Acceptance list is filtered by operating unit (record rule
  `performance_obligation_acceptance_rule_ou`): a user only sees records whose
  **Operating Unit** is one of the operating units assigned to them. Changing the field
  can therefore make a record disappear from, or reappear in, the current user's list.
  This is not a Flow step.

## Additional Post-Condition

- This model does not itself create any further document. However, because **Operating
  Unit** here is a writable `related` field mirroring the linked Performance Obligation,
  changing it on this Acceptance record writes the new value back onto that
  **Performance Obligation**'s own **Operating Unit** field — and from there it cascades
  to every other Acceptance and Revenue Recognition record sharing that same Performance
  Obligation. See `docs/performance_obligation/01-create.md` in this module.
