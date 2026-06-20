# CLAUDE.md

AI maintenance memory for the **ssi-revenue-recognition** repo. For the human-facing
overview and module list, see @README.md. For Odoo/SSI coding standards, the
authoritative source is the `/odoo-development` skill — this file does **not** restate
it.

## What this repo is

Odoo 14 addons implementing **revenue recognition per PSAK 115 (IFRS 15)** for SSI. Core
module `ssi_revenue_recognition` plus operating-unit / project / work-log / QC bridge
modules. Part of a Doodba multi-repo deployment (this is one independent sub-repo).

## ⏳ Active initiative — PSAK 115 remediation (multi-iteration)

There is an **ongoing, multi-iteration plan** to close PSAK 115 conceptual gaps and fix
existing bugs. **Before working on any revenue-recognition feature, read the plan
first:**

➡️ **[docs/psak115-remediation-plan.md](docs/psak115-remediation-plan.md)**

That file holds the gap analysis (G1–G7), the phased roadmap (Fase A/B + Priorities
1–3), locked design decisions, and a progress log. Keep its **Progress Log** updated as
work lands.

## Invariants — do NOT break

- **PoB is decoupled from `service.contract`.** Since migrations
  `14.0.5.0.0`→`14.0.7.0.0`, `performance_obligation` links to a contract only via
  `source_analytic_account_id` (an `account.analytic.account`). Do **not** reintroduce a
  direct `contract_id` field on the PoB. The originating contract is resolved through
  the shared analytic account.
- **`ssi_revenue_recognition_full` is deprecated / unusable** — do not use it as a
  reference or build on it.
- Never change existing XML IDs or rename existing Python classes/fields/models without
  an explicit instruction (see `/odoo-development`).
- **Do NOT bump the `version` in `__manifest__.py`** — a GitHub bot owns version
  numbers. The only exception: when you add a migration script under
  `migrations/<version>/`, you set the version to match that script's directory.

## Working conventions (delegated)

- Module structure, naming, security, views, manifests, unit tests →
  `/odoo-development`.
- Commit per module (`[ADD]`/`[UPD] module_name`), bump `version` in `__manifest__.py`,
  push via `rebase-repo.sh` + `push-odoo-module-revision.sh 14.0`. Never
  `git push`/`pull` directly. Details → `/odoo-development` →
  `references/git-workflow.md`.
- Install/test commands run in Docker from the deployment root (`${ODOO_DEV_PATH}`),
  e.g. `invoke install -m ssi_revenue_recognition`. Details → `/odoo-development`.

## Gotchas

- Schema-changing work on `ssi_revenue_recognition` needs a migration script under
  `migrations/<version>/`; the existing `14.0.5.0.0`–`14.0.7.0.0` scripts show the
  decoupling/rename pattern (model rename + stored-related recompute) — follow it.
