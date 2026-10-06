---
name: company-snapshot
description: Produces a short profile of one company — identity, size, financial headline and digital footprint — without the full KYB dossier. Use when the user asks "what is this company", "tell me about", "look up" or "profile" a company, or pastes a company website or LinkedIn URL and asks who they are.
---

# Company Snapshot

A fast read on a single company. This is the light path: identity, headline
financials and digital footprint, in one screen. When the user asks for due
diligence, a KYB check or anything compliance-shaped, use
`company-due-diligence` instead — it pulls the official registry record.

Never infer a missing value. Report it as `Not Available`.

## Trigger Examples

- What is acme.com?
- Tell me about Acme Ltd.
- Look up this company: linkedin.com/company/acme
- Profile Acme before the call.

## Workflow

1. **Resolve the entity, once.**
   - Website → `get_company_by_website`.
   - LinkedIn URL → `get_company_by_linkedin`.
   - Anything else (name, registration number, VAT, ticker, email) →
     `get_company_by_identifiers`.
   - If several companies come back, show name, country and registration number
     in a short table and ask which one before continuing.
   - Keep the resulting `company_id` and reuse it for every later call. Do not
     re-resolve.

2. **Profile.** `get_company_details` for the firmographic record.

3. **Financials.** `get_company_financials`. Report **the latest year and one
   prior** — nothing more. The payload carries every year on file and dumping it
   all buries the answer.

4. **Digital footprint.** `get_digital_insights` for traffic, ranking and
   technology stack. Skip this step if the user only asked "who are they".

## Report Layout

```
# <Legal Name>

<one-sentence description of what the company does>

| | |
|---|---|
| Country | |
| Founded | |
| Employees | |
| Industry | |
| Website | |

## Financials
Latest year vs prior: revenue, net profit, total assets.

## Digital
Traffic rank, main technologies.

## Sources
```

## Rules

- Resolve **once**; reuse the same `company_id`.
- Do not call `kyb_*` tools here. Those belong to `company-due-diligence`, cost
  a registry lookup, and are not what the user asked for.
- Never compute a column the payload does not contain. If revenue per employee
  is wanted, say it is derived and show the two inputs.
- Cite the source for every figure that carries one.
- If a step errors, retry up to 3 times, then mark that section `Not Available`
  and continue. Do not abandon the snapshot.
