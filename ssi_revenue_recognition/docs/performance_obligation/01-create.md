# Create Performance Obligation

> **Module:** ssi*revenue_recognition **Model:** `performance_obligation` > **Menu:**
> Cost Accounting > Revenue Recognition > Performance Obligations **Actor:** user in
> group \_Performance Obligation — User* > **State:** `—` → `draft`

## Pre-Condition

- **Data:** A contract's `account.analytic.account` (the **Source Analytic Account**)
  already exists — the Performance Obligation (PoB) will own an analytic account created
  below it once the PoB is opened.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model, used when the PoB
  reaches **Open**.
- **Access:** User is in group _Performance Obligation — User_.

## Flow

1. Open the **Cost Accounting > Revenue Recognition > Performance Obligations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Source Analytic Account**: Select the contract's analytic account this PoB
     belongs to.
   - **Title**: Enter a title for the promised good or service. Automatically filled
     from **Product**, if selected. Change if needed.
   - **Revenue Recognition Timing**: Select **Over Time** or **At a Point in Time**.
   - **Progress Completion Method**: Select **Input** or **Output**. Hidden when
     **Revenue Recognition Timing** is **At a Point in Time**.
   - **Date Start** / **Date End** _(required if **Revenue Recognition Timing** is **At
     a Point in Time**)_: Only shown and required for that timing.
4. On the **Transaction Price Allocation** tab, fill in:
   - **Currency**: Select the currency used to price this PoB.
   - **Product**: Select the promised good or service, if applicable.
   - **UoM Quantity**: Enter the promised quantity.
   - **UoM**: Automatically filled from **Product**. Change if needed.
   - **Pricelist**: Select the pricelist used to derive the unit price, if applicable.
   - **Price Unit**: Enter the unit price.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
