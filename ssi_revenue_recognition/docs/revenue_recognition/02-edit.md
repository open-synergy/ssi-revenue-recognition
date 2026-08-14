# Edit Revenue Recognition

> **Module:** ssi*revenue_recognition **Model:** `revenue_recognition` > **Menu:** Cost
> Accounting > Revenue Recognition > Revenue Recognitions **Actor:** user in group
> \_Revenue Recognition — User* > **Requires:** `01-create` > **Inline Actions:** >
> `action_populate` (Populate)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Revenue Recognition — User_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Revenue Recognitions** menu.
2. Find and open the record to edit.
3. Click the **Edit** button.
4. Change the required fields.
5. Click **Populate** to refresh the linked Performance Obligation Acceptances and WIP
   transactions — for example after changing **Date** or **Date Start**/**Date End**.
   Running it again releases the previous claim and re-links acceptances/WIP
   transactions against the new criteria; skipping it leaves the lists matching the old
   dates.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
