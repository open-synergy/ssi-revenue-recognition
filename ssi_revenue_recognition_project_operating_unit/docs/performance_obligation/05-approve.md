# Approve Performance Obligation

> **Module:** ssi_revenue_recognition_project_operating_unit
>
> **Extends:** ssi_revenue_recognition_project — model `performance_obligation`, aksi
> `05-approve`

## Additional Post-Condition

- When the Approve action reaches **Open** and a `project.project` is created (or
  refreshed) as documented by the extended module's own
  `docs/performance_obligation/05-approve.md`, that project's **Operating Unit** follows
  the PoB's own **Operating Unit** — not the acting user's default, not the project's
  previous value. This is not a Flow step; it runs automatically as part of the same
  Approve action, inside the project-creation side effect owned by
  `ssi_revenue_recognition_project`.
