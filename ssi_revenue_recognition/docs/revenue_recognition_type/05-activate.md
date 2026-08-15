# Activate Revenue Recognition Type

> **Module:** `ssi_revenue_recognition`
>
> **Model:** `revenue_recognition_type`
>
> **Menu:** Cost Accounting > Configuration > Revenue Recognition > Revenue Recognition
> Types
>
> **Actor:** user in group _Revenue Recognition Type — Configurator_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Revenue Recognition Type — Configurator_.

## Flow

1. Open the **Cost Accounting > Configuration > Revenue Recognition > Revenue
   Recognition Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected as the **Type** of a new `revenue_recognition` document.
