# Cancel Performance Obligation

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `performance_obligation`
>
> **Menu:** Cost Accounting > Revenue Recognition > Performance Obligations
>
> **Actor:** user in group _Performance Obligation — User_
>
> **State:** `draft` | `open` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **Open**.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Data:** At least one `base.cancel_reason` is configured for this model.
- **Access:** User is in group _Performance Obligation — User_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Performance Obligations** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
