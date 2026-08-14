# Deactivate Revenue Recognition Type

> **Module:** ssi*revenue_recognition **Model:** `revenue_recognition_type` > **Menu:**
> Cost Accounting > Configuration > Revenue Recognition > Revenue Recognition Types
> **Actor:** user in group \_Revenue Recognition Type — Configurator* > **Active:** >
> `true` → `false` > **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Revenue Recognition Type — Configurator_.

## Flow

1. Open the **Cost Accounting > Configuration > Revenue Recognition > Revenue
   Recognition Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected as the **Type** of a new `revenue_recognition`
  document.
- `revenue_recognition` documents that already use this type can still be viewed.
