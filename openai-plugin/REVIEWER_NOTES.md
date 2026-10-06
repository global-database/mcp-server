# Global Database — notes for the ChatGPT plugin review

Plugin `plugin_asdk_app_696f807d21a481918a1ed1f43d719ce9` · MCP app `asdk_app_696f807d21a481918a1ed1f43d719ce9`
· server `https://mcp.globaldatabase.com/mcp` · Platform organization `org-7r5YlU215AVPzyoRSYatteiY`

These notes cover the seven tool updates held with "needs further review" and the server
instructions. Every statement about a tool below is taken from the tool definitions the server
publishes; nothing here describes behaviour the tools do not have.

## How access works

- **Per-user OAuth 2.1** (authorization code + PKCE, Dynamic Client Registration). Each ChatGPT
  user signs in with their own Global Database account; there is no shared key.
- **Every call runs under that user's own subscription.** The server forwards the user's token;
  what a call returns is limited by that account's plan and permissions. Extended contact fields
  in `enrich_employee_contacts`, for example, are returned only when the account holds the
  Contact Details permission — without it they are absent.
- **All 23 tools are read-only.** Annotations on every tool: `readOnlyHint: true`,
  `destructiveHint: false`, `idempotentHint: true`. Nothing creates, updates, deletes or sends.
- **Demo account for reviewers:** `<email — to fill>` / `<password — to fill>` — a full-access
  Global Database account, separate from customer accounts.

## The seven held tools

| Tool | What it returns about people | Minimisation built in |
|---|---|---|
| `search_employees` | For people at a company or matching a role/name: `id, name, company_id, company_name` | Those four fields only — **no contact details**. Requires at least one filter. |
| `get_employee_details` | One selected person's profile: name, gender, nationality, seniority, department, job title, business phone and email, company, LinkedIn/Twitter/Facebook | One person per call, for the row the user picked. Batch only when the user explicitly asks for several or all rows; the model is told never to fan out on its own initiative. |
| `enrich_employee_contacts` | One named contact's business email and phone, job details and social profiles | Needs an exact identifier (email, LinkedIn URL, or name + company/domain). The model is told to present only what the user asked for. |
| `find_people_by_domain` | People at a company given its web domain: name, job title, seniority, LinkedIn, city/state/country | **No email or phone** in this tool. Requires a filter (the domain). |
| `kyb_officers_search` | Company officers matching a name, from registry filings: role, appointment/resignation dates, nationality, **birth year only**, registered address, email where filed | Name is required. Registry officer data, used for KYB/compliance. |
| `kyb_shareholders_search` | Companies a named shareholder (person or company) holds stakes in: holding percentage, share details | Name is required. A `lite` view returns holder and company only. Used for beneficial-ownership checks. |
| `get_digital_insights` | Company web presence; includes the domain's WHOIS record | Company-level tool, takes a `company_id` from a previous lookup. |

What the tools never handle: payment card data, health data, government ID numbers, or anyone's
passwords or authentication secrets.

## Purpose

The plugin answers business-to-business questions: verifying a company and who runs and owns it
(KYB / compliance), and finding the right business contact at a company (sales prospecting).
People data is returned only as part of those flows and only when the user asks about a person
or a role.

## Server instructions

The instructions exist to stop the model from inventing company or person data: every name,
figure and identifier in a reply must come from a tool result, and an empty result is reported
as such. Two wordings flagged by the scan on 2026-10-05 were reworded the same day ("You are a
business intelligence assistant powered by…", "You know nothing about any company…"); the
"compare/prefer" finding no longer appears after rescanning.

## Contact

Support: https://globaldatabase.com/contact-us · Technical: ion.ghiderman@globaldatabase.com
