---
name: prospect-list
description: Builds a target account list from firmographic filters — country, industry, size, revenue — then optionally finds and enriches contacts at each company. Use when the user asks to find, search or build a list of companies matching criteria, to source leads or accounts, or to get contacts at a set of companies.
---

# Prospect List

Turn a description of an ideal customer into a concrete list of companies, and
optionally into named contacts. One company is a job for `company-snapshot`;
this skill is for sets.

## Trigger Examples

- Find SaaS companies in Germany with 50–200 employees and over €10M revenue.
- Build me a list of UK fintechs founded after 2020.
- Who should we target in the Nordics for logistics software?
- Get me contacts at these 20 accounts.

## Workflow

1. **Settle the filters before searching.** Restate the criteria back to the
   user as a short list and confirm anything they left open — country, industry,
   employee band, revenue band, founding year. A vague search burns a call and
   returns noise.

2. **Resolve filter values.** Call `get_nomenclature` to get the accepted values
   for industry, country and any coded field. Do **not** guess a code or pass a
   free-text industry name — filters are matched against the nomenclature, and an
   invented value silently returns nothing rather than erroring.

3. **Search.** Call `prospecting` with the resolved filters. Report how many
   companies matched **before** listing any. If the count is very large, say so
   and offer to tighten the filters rather than paging through it.

4. **Present the list.** One row per company: name, country, industry,
   employees, revenue, website. Stop at 25 rows unless the user asked for more,
   and say how many were withheld.

5. **Contacts — only if asked.** Do not go looking for people unless the user
   wants them.
   - For a company already resolved: `search_employees`, filtered by role or
     seniority when the user named one.
   - Starting from a domain instead: `find_people_by_domain`.
   - For a full profile of one person: `get_employee_details`.
   - `enrich_employee_contacts` returns email and phone. Call it **per contact
     the user actually wants**, not across the whole list — it is the expensive
     step and most rows will never be worked.

## Report Layout

```
# Target list — <criteria in one line>

<N> companies matched. Showing <M>.

| Company | Country | Industry | Employees | Revenue | Website |
|---|---|---|---|---|---|

## Contacts (if requested)
| Company | Name | Role | Email | Phone |
```

## Rules

- Never invent a filter value. Resolve it through `get_nomenclature` first.
- Never fabricate an email address or phone number. If enrichment returns
  nothing, the cell is `Not Available` — a plausible-looking guess at a work
  email is worse than a blank.
- State the match count before the rows, and state what was truncated.
- Enrich contacts one at a time, on request. Do not bulk-enrich a list.
- If the search returns zero, say which filter is most likely responsible and
  propose a specific loosening — do not silently retry with different criteria.
