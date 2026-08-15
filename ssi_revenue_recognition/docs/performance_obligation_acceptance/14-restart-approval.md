# Restart Approval Process — Performance Obligation Acceptance

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `performance_obligation_acceptance`
>
> **Menu:** Cost Accounting > Revenue Recognition > Performance Obligation Acceptances
>
> **Actor:** user in group _Performance Obligation Acceptance — Validator_
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `restart_approval_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group _Performance Obligation Acceptance — Validator_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Performance Obligation
   Acceptances** menu.
2. Open the record whose approval process will be restarted.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- Existing approval records are discarded and recreated from the approval template, so
  the approval process starts again from the first level.
