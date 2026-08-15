# Create Performance Obligation Acceptance

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `performance_obligation_acceptance`
>
> **Menu:** Cost Accounting > Revenue Recognition > Performance Obligation Acceptances
>
> **Actor:** user in group _Performance Obligation Acceptance — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `performance_obligation` document exists in status **Open** (or **Done**)
  for the customer, so it can be selected.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Performance Obligation Acceptance — User_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Performance Obligation
   Acceptances** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Partner**: Select the customer accepting the fulfilled quantity/progress.
   - **Contact**: Select the contact person, if applicable.
   - **# Performance Obligation**: Select the PoB (filtered to the selected **Partner**)
     this acceptance is for.
   - **Date**: Enter the acceptance date.
   - **Date Start** / **Date End**: Enter the period covered by this acceptance.
4. On the **Manual Fulfillments** tab, add lines when the PoB's **Fulfillment Field** is
   configured to read manual entries. Repeat the following steps as many times as
   needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Product**: Select the product/service fulfilled, if applicable.
     - **UoM Quantity**: Enter the fulfilled quantity.
     - **UoM**: Automatically filled from **Product**. Change if needed.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
