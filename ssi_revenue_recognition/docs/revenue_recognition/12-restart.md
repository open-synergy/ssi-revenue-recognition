# Restart Revenue Recognition

> **Module:** ssi*revenue_recognition **Model:** `revenue_recognition` > **Menu:** Cost
> Accounting > Revenue Recognition > Revenue Recognitions **Actor:** user in group
> \_Revenue Recognition — Validator* > **State:** `cancel` | `reject` → `draft` >
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group _Revenue Recognition — Validator_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Revenue Recognitions** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
