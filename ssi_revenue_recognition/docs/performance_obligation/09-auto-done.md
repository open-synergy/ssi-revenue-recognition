# Auto-Finish Performance Obligation

> **Module:** ssi_revenue_recognition **Model:** `performance_obligation` > **Menu:**
> Cost Accounting > Revenue Recognition > Performance Obligations **Actor:** System —
> triggered automatically, no user interaction **State:** `open` → `done` >
> **Requires:** `05-approve`

There is no **Done** button on this model (`_automatically_insert_done_button = False`).
The transition to **Done** is performed automatically by a `base.automation` rule
(`pob_open_2_done`) whenever the PoB is written to and its computed **Quantity Diff.**
reaches `0.0` while the record is **Open**.

## Pre-Condition

- **Record:** Status is **Open**.
- **Record:** At least one **Performance Obligation Acceptance** for this PoB has
  reached status **Done**, so **Quantity Accepted** can equal **UoM Quantity**.

## Flow

This transition has no click steps — it is triggered automatically by the system. A user
records (and completes the approval of) a **Performance Obligation Acceptance** for this
PoB whose accepted quantity brings the PoB's **Quantity Diff.** field down to `0.0` —
see `docs/performance_obligation_acceptance/05-approve.md`. Writing the acceptance
recomputes the PoB's stored **Quantity Diff.** field, which in turn re-evaluates the
`base.automation` rule `pob_open_2_done`.

## Post-Condition

- Status changes to **Done**.
