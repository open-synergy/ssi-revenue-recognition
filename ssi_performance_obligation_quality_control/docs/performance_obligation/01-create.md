# Create Performance Obligation

> **Module:** ssi_performance_obligation_quality_control
>
> **Extends:** ssi_revenue_recognition — model `performance_obligation`, action
> `01-create`

## Modified Flow

- Anchor: visible on the form from the moment it opens (before step 3 of the base Flow),
  and present in every status afterward — because this module sets
  `_qc_worksheet_create_page = True`, a **Quality Control** tab is added by
  `mixin.qc_worksheet` (`ssi_quality_control`). It can be filled in **any status**; the
  mixin does not restrict it to Draft. It holds:
  - **Worksheet Set**: an editable field to pick the `qc_worksheet_set_id` template used
    to auto-generate worksheets for this PoB via the **Create Worksheet From Set**
    button. Optional, no default.
  - **Result Computation Method**: an editable **Automatic**/**Manual** selection.
    Defaults to **Automatic**.
  - Read-only **Automatic** and **Final** result indicators, and an editable **Manual**
    result checkbox (only meaningful when **Result Computation Method** is **Manual**).
  - **Create Worksheet From Set** and **Open QC Worksheet** buttons, plus an embedded
    **QC Worksheets** list.
  - Creating, answering, and completing the worksheets themselves — including what the
    two buttons above do — is governed by the `ssi_quality_control` module; this
    extension does not repeat those steps.
