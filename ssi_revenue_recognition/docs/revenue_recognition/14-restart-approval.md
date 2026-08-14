# Restart Approval Process — Revenue Recognition

> **Module:** ssi*revenue_recognition **Model:** `revenue_recognition` > **Menu:** Cost
> Accounting > Revenue Recognition > Revenue Recognitions **Actor:** user in group
> \_Revenue Recognition — Validator* > **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `restart_approval_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group _Revenue Recognition — Validator_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Revenue Recognitions** menu.
2. Open the record whose approval process will be restarted.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- Existing approval records are discarded and recreated from the approval template, so
  the approval process starts again from the first level.
