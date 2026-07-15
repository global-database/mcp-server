---
name: company-due-diligence
description: Runs a structured KYB / due-diligence review of a company — resolves the entity, then pulls official-registry details, directors, shareholders, corporate group structure and financials into one report. Use when the user asks to run due diligence, a KYB check, a compliance review, or to "check out" / "vet" a company.
---

# Company Due Diligence

Produce a consistent KYB dossier for a single company from Global Database. Resolve
the entity once, then gather registry and financial facts and present them as a
structured report. Never infer missing values — state them as `Not Available`.

## Trigger Examples

- Run due diligence on Acme Ltd.
- Do a KYB check on acme.com.
- Vet this company before we onboard them: Acme Ltd, UK.

## Workflow

1. **Resolve the entity.**
   - If the user gave a website or LinkedIn URL, use `get_company_by_website` or
     `get_company_by_linkedin`.
   - Otherwise use `get_company_by_identifiers` (name, registration number, VAT,
     ticker, email) to obtain a `company_id`.
   - If multiple matches come back, show them in a short table (name, country,
     registration number) and ask the user to pick one before continuing.

2. **Official registry record.** Call `kyb_search` if you still need the registry
   identifier, then `kyb_company_details` for the authoritative registry record
   (legal name, status, incorporation date, registered address).

3. **People.** Call `kyb_officers` for directors, secretaries and officers. Flag any
   officer whose status is not active.

4. **Ownership.** Call `kyb_shareholders` for shareholders and `kyb_group_structure`
   for the corporate group. Note any ownership the registry marks as beneficial.

5. **Financials.** Call `kyb_financial` for filed statements across years. If the
   registry has none, fall back to `get_company_financials`. Report the latest year
   plus one prior for trend.

6. **Assemble the dossier** using the report layout below.

## Progress Display

Before each step, reprint the stepper with the entity name as a subtitle, e.g.
`> Due diligence for **Acme Ltd**`. Icons: ✅ done · ⏳ in progress · ⬜ not started
· ❌ failed.

```
⬜ Step 1: Resolving Entity
⬜ Step 2: Registry Record
⬜ Step 3: Officers
⬜ Step 4: Ownership
⬜ Step 5: Financials
⬜ Step 6: Report
```

## Report Layout

```
# Due Diligence — <Legal Name>

## Identity
- Registry status, registration number, incorporation date, registered address

## Officers
- One row per officer: name, role, appointed date, status

## Ownership
- Shareholders with % held; group parent/subsidiaries if any

## Financials
- Latest year vs prior: revenue, net profit, total assets, key ratios

## Flags
- Anything notable: inactive status, resigned officers, missing filings
```

## Rules

- Resolve the entity **once**; reuse the same `company_id` for every later call.
- Do not call tools the workflow does not list unless the user explicitly asks.
- If a step returns an error, retry up to 3 times, then record that section as
  `Not Available` and continue — do not abort the whole dossier.
- Never fabricate registry numbers, ownership percentages or financial figures.
