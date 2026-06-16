# Rencana Perbaikan PSAK 115 — ssi-revenue-recognition

Dokumen kerja **multi-iterasi** untuk menutup gap konsep PSAK 115 (IFRS 15) dan
memperbaiki bug pada modul revenue recognition. Dibaca AI & tim sebelum mengerjakan
fitur revenue recognition. Pintu masuk: [CLAUDE.md](../CLAUDE.md).

> Status keseluruhan: **PERENCANAAN** — belum ada kode yang ditulis. Lihat
> [Progress Log](#progress-log) di bagian akhir.

---

## 1. Konteks

Modul mengeksekusi tulang punggung PSAK 115 dengan benar di **Langkah 2 (identifikasi
performance obligation)** dan **Langkah 5 (pengakuan)**. Gap utama ada di **Langkah 3
(harga transaksi)**, **Langkah 4 (alokasi)**, serta beberapa konsep pendukung.

Lima langkah PSAK 115: (1) ada kontrak, (2) pecah jadi janji/PoB, (3) tentukan total
harga, (4) bagi harga ke tiap janji, (5) akui pendapatan saat janji dipenuhi.

### Status per langkah

| Langkah                 | Diminta PSAK 115                        | Status modul                                                     |
| ----------------------- | --------------------------------------- | ---------------------------------------------------------------- |
| 1. Identifikasi kontrak | Cek kontrak sah & pelanggan mampu bayar | Setengah — diwakili `account.analytic.account`, tanpa cek formal |
| 2. Identifikasi PoB     | Pecah kontrak jadi janji terpisah       | **Sudah ada** (manual)                                           |
| 3. Tentukan harga       | Termasuk harga variabel & estimasi      | Setengah — hanya `price_unit × qty`                              |
| 4. Alokasi harga ke PoB | Bagi total ke tiap janji (SSP)          | **Belum ada**                                                    |
| 5. Akui pendapatan      | Sekaligus / bertahap                    | **Sudah ada** (lihat G3 untuk metode biaya)                      |

---

## 2. Gap Analysis (G1–G7, urut dampak)

### G1 — Hanya mendukung "tagih dulu, akui kemudian" (tidak ada Contract Asset)

Jurnal selalu `Dr Unearned Income / Cr Pendapatan` → mengasumsikan penagihan/bayar di
muka (deferred revenue release). Skenario **earned-but-unbilled** (kerja dulu, tagih
kemudian → timbul **Contract Asset / accrued revenue**) tidak didukung. PSAK 115
mewajibkan membedakan contract asset vs contract liability. **Gap fundamental.**

### G2 — Alokasi harga ke tiap PoB belum ada (Langkah 4) — _= D1, disetujui_

Harga tiap PoB diisi manual; tak ada pembagian total kontrak ke tiap janji berdasarkan
standalone selling price. Contoh: bundel Rp100jt (training + maintenance) harus dibagi
proporsional.

### G3 — Metode "bertahap berdasarkan biaya" (cost-to-cost) setengah jadi — _quick win_

Mesin % penyelesaian dari biaya **sudah ada** (`amount_budgeted`, `amount_realized`,
`percent_realized`, `theoritical_accepted` di `revenue_recognition._compute_budget`),
tapi `income_amount_policy` **hanya** menyediakan `amount_accepted` (output/qty
acceptance). Opsi "akui pendapatan sesuai % biaya" (input method) belum tersedia untuk
pendapatan — angka cost-to-cost baru dipakai sisi expense. Effort kecil.

### G4 — Harga variabel (bonus/penalti/diskon kondisional) — _= D3, disetujui (dengan metode)_

Tidak bisa memasukkan estimasi bonus/penalti + batas kehati-hatian (constraint).
Disepakati memakai metode PSAK 115 (`expected_value` vs `most_likely_amount`).

### G5 — Biaya kontrak (incremental cost & cost to fulfill) tidak dikapitalisasi

Komisi memperoleh kontrak / biaya mobilisasi awal seharusnya bisa jadi aset lalu
diamortisasi seiring pendapatan. Belum ada.

### G6 — Modifikasi kontrak — _= D2_

Perubahan scope/harga di tengah kontrak belum ditangani. Aturan rumit (prospektif vs
penyesuaian kumulatif) → butuh dokumen desain tersendiri.

### G7 — Dokumentasi judgment & laporan pengungkapan

Alasan memilih "diakui bertahap" tidak disimpan (auditabilitas). Belum ada laporan
backlog (sisa nilai PoB) & disagregasi pendapatan.

### Konsep PSAK 115 lain yang belum ada (Prioritas 3, perlu konfirmasi kebutuhan bisnis)

Significant financing component; garansi assurance vs service-type; principal vs agen;
lisensi right-to-access vs right-to-use; material right / opsi pelanggan; non-refundable
upfront fees; penilaian "distinct" & "series of distinct".

---

## 3. Keputusan desain terkunci

| Kode    | Keputusan                                                                                                                                                                                                                                                                   |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1 (G2) | Total harga transaksi kontrak diambil dari `account.analytic.account.pob_planned_amount`. Alokasi PoB = `(standalone_selling_price PoB / Σ standalone pada AA yang sama) × pob_planned_amount`. Selektor `transaction_price_basis` default `pob_price` agar data lama aman. |
| D3 (G4) | Variable consideration memakai metode PSAK 115: field `variable_consideration_method` (`expected_value` / `most_likely_amount`) + `constraint_amount` (cap).                                                                                                                |

---

## 4. Bug yang harus diberesi lebih dulu (fondasi)

Dikerjakan **sebelum** fitur PSAK 115. Tiap modul = commit terpisah.

> **Versi modul:** JANGAN ubah `version` di `__manifest__.py` — diurus bot GitHub.
> Satu-satunya pengecualian: saat menambah migration script (mis. G2/D1), set versi
> menyamai folder `migrations/<versi>/`.

### Fase A — `ssi_revenue_recognition`

- **A1 — DIBATALKAN (bukan bug).** `performance_obligation._compute_quantity_accepted`
  menjumlahkan `qty_fulfilled` (tak di-cap), sedangkan `revenue_recognition` memakai
  `qty_accepted` (di-cap). Keduanya **identik di operasi normal**; berbeda hanya saat
  over-fulfillment (kumulatif > total PoB). Jurnal pendapatan dibuat dari
  `revenue_recognition` (sudah di-cap) → tidak ada dampak akunting;
  `PoB.amount_accepted` hanya display. Dipertahankan apa adanya (menampilkan
  over-delivery > 100% disengaja). Re-aktifkan hanya bila diminta meng-cap tampilan PoB.
- **A2** `revenue_recognition_type.py:25`: label `income_usage_id` `string=` dari
  `"Unearned Income Usage"` → `"Income Usage"` (label saja, bukan rename field).
- **A3** Ganti `try/except Exception` / `except: pass` guard pembagian di
  `revenue_recognition._compute_quantity_accepted`, `_compute_budget`, dan
  `revenue_recognition_account._compute_percent_realized` dengan guard `if divisor:`.
- **A4 — DIBATALKAN.** `performance_obligation.onchange_name` (`pass`) **sengaja**
  meng-override onchange dari mixin agar `name` tidak terisi otomatis. Jangan dihapus.

### Fase B — modul jembatan (commit per modul, tanpa ubah versi)

- **B1** `ssi_service_revenue_recognition`: `env.ref(xmlid)` di
  `service_contract_fix_item._prepare_pob_data` pakai `raise_if_not_found=False` +
  `UserError` terstruktur bila field tak ketemu (cegah crash).
- **B2** `ssi_batch_project_assignment_revenue_recognition`: hapus `.pot` duplikat
  `i18n/ssi_project_assignment_revenue_recognition.pot`.
- **B3 — DIBATALKAN.** Pembuatan `.pot` adalah tugas GitHub Action
  (`oca_export_and_push_pot` di `test.yml`); standar SSI melarang membuat `.pot`/`.po`
  manual di lokal. Tidak ada tindakan.
- **B4 — DIBIARKAN (keputusan user).** Duplikasi `_compute_revenue_recognition_field` di
  dua modul project assignment; tiap method menempel di model berbeda, mengangkat ke
  mixin lintas-modul tak sepadan. Tidak ada tindakan.
- **B5 — DIBIARKAN (keputusan user).** Group view kosong `revenue_recognition_1_2`
  dibiarkan apa adanya. Tidak ada tindakan.

---

## 5. Roadmap berprioritas

### 🟢 Prioritas 1 (dampak tinggi) — lihat detail di §6

1. **Fase A** (bug inti)
2. **Fase B** (bug jembatan)
3. **G3** — aktifkan input method (cost-to-cost) untuk income
4. **G2 / D1** — alokasi harga ke PoB
5. **G1** — dukungan Contract Asset (sub-fase, mengubah pola jurnal)

### 🟡 Prioritas 2 (setelah P1 stabil)

- **G4 / D3** — harga variabel + metode + constraint
- **G5** — kapitalisasi & amortisasi biaya kontrak
- **G7** — simpan alasan pengakuan + laporan backlog/disagregasi

### 🔴 Prioritas 3 (butuh dokumen desain dulu, belum dikoding)

- **G6 / D2** — modifikasi kontrak
- Financing component, garansi, principal/agen, lisensi, material right, upfront fees,
  penilaian distinct/series

---

## 6. Detail Prioritas 1

> Diisi/diperbarui saat eksekusi dimulai. Ringkasan rencana per langkah:

### P1.1 — Fase A & B

Lihat §4. Kerjakan, install per modul (`invoke install -m <module>`), smoke test manual.

### P1.2 — G3: input method (cost-to-cost) untuk income

- Tambah opsi `theoritical_accepted` pada selection `income_amount_policy` di
  `revenue_recognition` (sudah ada field `theoritical_accepted` hasil
  `_compute_budget`).
- Verifikasi `_prepare_income_ml` / `_prepare_unearned_income_ml` memakai
  `getattr(self, self.income_amount_policy)` → otomatis ikut.
- Tidak ada perubahan skema → tidak ada migration & tidak ubah versi; uji jurnal manual.

### P1.3 — G2 / D1: alokasi harga

- Field baru PoB: `standalone_selling_price` (Monetary, editable draft).
- Field computed PoB: `allocated_transaction_price` (basis `pob_planned_amount`, rumus
  §3).
- Selektor `transaction_price_basis` (`pob_price` default / `allocated`) di
  `revenue_recognition`; basis dipakai pada perhitungan `amount_accepted`.
- Tombol "Recompute Allocation" di `account.analytic.account`.
- Perubahan skema → **butuh migration script**; ini satu-satunya titik di P1 yang
  mengubah `version` (samakan dengan folder `migrations/<versi>/`, mis. 14.0.9.0.0).

### P1.4 — G1: Contract Asset

- Sub-fase tersendiri karena mengubah pola jurnal.
- Rancangan awal: tambah arah pengakuan saat earned > billed (Dr Contract Asset / Cr
  Pendapatan), dengan akun contract asset di `revenue_recognition_type`.
- **Butuh konfirmasi desain sebelum koding** (pola jurnal & reklas saat penagihan).

---

## Progress Log

Catat tiap perubahan yang landing (tanggal, fase, modul, versi, ringkasan). Format:
`YYYY-MM-DD — <fase> — <module> v<versi> — <ringkasan>`.

- 2026-06-14 — Perencanaan — dokumen rencana & CLAUDE.md dibuat. Belum ada kode.
- 2026-06-14 — Fase A — `ssi_revenue_recognition` (versi tetap 14.0.8.0.0, tanpa
  migration) — A2 (label `income_usage_id` → "Income Usage") + A3 (guard pembagian
  `if divisor:` di `_compute_quantity_accepted`, `_compute_budget`,
  `revenue_recognition_account._compute_percent_realized`). A1 & A4 dibatalkan.
  Verifikasi `odoo -u` lolos (511 modul loaded, tanpa error). Commit `17431af`. Belum
  di-push.
- 2026-06-14 — Fase B — B1 `ssi_service_revenue_recognition` (repo opnsynid-service,
  commit `1dbe7ac`): guard `env.ref` + `UserError` terstruktur. B2
  `ssi_batch_project_assignment_revenue_recognition` (repo opnsynid-project, commit
  `7b3e2b8`): hapus `.pot` salah tempat. B3 dibatalkan (tugas GH Action); B4 & B5
  dibiarkan (keputusan user). Verifikasi `odoo -u ssi_service_revenue_recognition`
  lolos. Belum di-push.
