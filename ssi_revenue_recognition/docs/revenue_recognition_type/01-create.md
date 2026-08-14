# Create Revenue Recognition Type

> **Module:** ssi*revenue_recognition **Model:** `revenue_recognition_type` > **Menu:**
> Cost Accounting > Configuration > Revenue Recognition > Revenue Recognition Types
> **Actor:** user in group \_Revenue Recognition Type — Configurator* > **State:** `—` →
> `draft` > **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Data:** An `account.journal` exists to receive the accounting entries posted by
  documents of this type.
- **Data:** Two `product.usage_type` records exist — one to resolve the unearned income
  account, one to resolve the income account.
- **Access:** User is in group _Revenue Recognition Type — Configurator_.

## Flow

1. Open the **Cost Accounting > Configuration > Revenue Recognition > Revenue
   Recognition Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name**: Enter a descriptive name for the type.
   - **Code**: Leave as **/** to generate it automatically, or type a code manually.
   - **Journal**: Select the journal used to post the accounting entry.
   - **Unearned Income Usage**: Select the product usage code that resolves the unearned
     income account.
   - **Income Usage**: Select the product usage code that resolves the income account.
4. On the **Accounting** tab, add one or more lines in **Account Mapping**. Repeat the
   following steps as many times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **WIP Account**: Select the WIP account for this mapping.
     - **Expense Account**: Select the expense account for this mapping.
5. Click **Generate Code** to assign a document code from the sequence, if the **Code**
   field is still **/**. You may also type a code manually instead. **Delete**
   (03-delete) requires the code to still be **/**, so only generate/enter a permanent
   code once the type is finalised.
6. Click **Save**.

## Post-Condition

- A new record is created and active.
