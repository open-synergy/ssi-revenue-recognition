# Approve Performance Obligation Acceptance

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `performance_obligation_acceptance`
>
> **Menu:** Cost Accounting > Revenue Recognition > Performance Obligation Acceptances
>
> **Actor:** approver on the approval level that is currently pending
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Performance Obligation
   Acceptances** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, the record is automatically finished (method
  `action_done`): status changes to **Done**, and its fulfilled quantity becomes
  eligible to be picked up by a `revenue_recognition` document.
