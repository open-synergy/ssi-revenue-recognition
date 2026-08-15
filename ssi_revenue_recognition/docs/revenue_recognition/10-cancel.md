# Cancel Revenue Recognition

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `revenue_recognition`
>
> **Menu:** Cost Accounting > Revenue Recognition > Revenue Recognitions
>
> **Actor:** user in group _Revenue Recognition — Validator_
>
> **State:** `draft` | `confirm` | `done` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Data:** At least one `base.cancel_reason` is configured for this model.
- **Access:** User is in group _Revenue Recognition — Validator_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Revenue Recognitions** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If an accounting entry (**# Move**) had already been posted (i.e. the record was
  **Done**), it is unposted, deleted, and the **# Move** field is cleared.
