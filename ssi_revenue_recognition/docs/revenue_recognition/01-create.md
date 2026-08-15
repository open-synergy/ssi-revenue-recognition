# Create Revenue Recognition

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `revenue_recognition`
>
> **Menu:** Cost Accounting > Revenue Recognition > Revenue Recognitions
>
> **Actor:** user in group _Revenue Recognition — User_
>
> **State:** `—` → `draft`
>
> **Inline Actions:** `action_populate` (Populate)

## Pre-Condition

- **Data:** A `revenue_recognition_type` is configured with its journal and account
  usages.
- **Data:** A `performance_obligation` document exists in status **Open** (or **Done**)
  for the customer, so it can be selected.
- **Data:** At least one `performance_obligation_acceptance` for that PoB has reached
  status **Done** and is not yet claimed by another Revenue Recognition document, so
  **Populate** has something to pull in.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _Revenue Recognition — User_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Revenue Recognitions** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields, in this order — **Partner** and **# Performance
   Obligation** first, so **Product** (via the selected PoB) is already known when
   **Type** is filled in and its Unearned Income/Income Account lookup runs:
   - **Partner**: Select the customer.
   - **# Performance Obligation**: Select the PoB (filtered to the selected **Partner**)
     this recognition is for.
   - **Type**: Select the `revenue_recognition_type` configuring the journal and account
     usages for this document.
   - **Journal**: Automatically filled from **Type**. Change if needed.
   - **Unearned Income Account**: Automatically filled from **Type** and **Product**
     (via the product's fiscal position). Change if needed.
   - **Income Account**: Automatically filled from **Type** and **Product**. Change if
     needed.
   - **Date**: Enter the recognition date.
   - **Date Start** / **Date End**: Enter the period of WIP transactions to consider.
4. On the **Accounting** tab, the **Account Mappings** grid is automatically rebuilt
   from **Type**'s configured WIP/expense account pairs whenever **Type** changes.
5. Click **Populate** to link the unclaimed, **Done** Performance Obligation Acceptances
   dated on or before **Date** to this record, and to refresh the WIP transactions dated
   within **Date Start**/**Date End** used to compute each account mapping's balance and
   budget. There is no manual way to fill these lists — **Populate** is the only way,
   and running it again re-evaluates the same criteria (safe to repeat, e.g. after
   changing **Date**). Skipping it leaves **Quantity Accepted**, **Amount Accepted**,
   and the **Accounting** tab's balances at zero.
6. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
