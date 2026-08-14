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
  acting user's own default operating unit. This field does not declare
  `readonly=False`, so — like every `related` field in Odoo unless it explicitly opts
  out — it is **read-only** on this record in every status: **Draft**, **Waiting for
  Approval**, and **Done** alike. It cannot be typed into or changed directly here; it
  only ever displays whatever value the linked **Performance Obligation** currently
  carries. See `## Additional Post-Condition` below for how that value is set.

## Modified — Record Visibility

- The Performance Obligation Acceptance list is filtered by operating unit (record rule
  `performance_obligation_acceptance_rule_ou`): a user only sees records whose
  **Operating Unit** is one of the operating units assigned to them. Because the field
  is read-only here, a record can only move between lists indirectly, by someone
  changing the **Operating Unit** on its linked **Performance Obligation** (see
  `docs/performance_obligation/01-create.md` in this module). This is not a Flow step.

## Additional Post-Condition

- This model does not itself create any further document. **Operating Unit** on this
  record is not set here — it is always the mirror of the linked **Performance
  Obligation**'s own **Operating Unit** field, and updates automatically whenever that
  source field changes. To change which operating unit an Acceptance belongs to, change
  it on the **Performance Obligation** instead; see
  `docs/performance_obligation/01-create.md` in this module.
