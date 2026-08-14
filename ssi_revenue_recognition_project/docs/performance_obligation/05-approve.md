# Approve Performance Obligation

> **Module:** ssi_revenue_recognition_project
>
> **Extends:** ssi_revenue_recognition — model `performance_obligation`, aksi
> `05-approve`

## Additional Post-Condition

- When **Auto Create Project** is checked, a `project.project` record is automatically
  created and linked via **Project** once the PoB reaches **Open** (`open`) — unless
  **Project** was already set, in which case that existing project is refreshed instead.
  When **Auto Create Project** is left unchecked (the default), this side effect does
  not run and **Project** stays empty. This is not a Flow step; it runs automatically as
  part of the same Approve action documented in the base module's
  `ssi_revenue_recognition/docs/performance_obligation/05-approve.md`.
