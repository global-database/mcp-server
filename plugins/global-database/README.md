# Global Database

Company intelligence, people search and KYB/compliance data from
[Global Database](https://globaldatabase.com/), for Claude.

This plugin connects Claude to the hosted Global Database MCP server at
`https://mcp.globaldatabase.com/mcp` and adds three skills that turn its tools into
complete workflows.

## What it does

- **Company profiles**: look a company up by website, LinkedIn, name, registration
  number, VAT or ticker, with per-section provenance.
- **Financials and ownership**: balance sheets, ratios and year-on-year metrics,
  shareholders and corporate group structure.
- **Digital insights**: web traffic, rankings, traffic sources, technology stack and WHOIS.
- **Prospecting**: filter companies by country, industry, size, revenue, growth and
  technology, then rank them.
- **People and contacts**: find employees by company or domain and resolve a named person
  to a verified work email and direct dial.
- **KYB / compliance**: registry details, officers, shareholders, group structure and filed
  financials from official government registries, plus reverse search of a person across
  jurisdictions.

All 23 tools are read-only. The server performs no writes, sends no email and takes no
action on the user's behalf.

## Skills

| Skill | Use it for |
|---|---|
| `company-snapshot` | A short profile of one company: identity, size, financial headline, digital footprint. |
| `company-due-diligence` | A full due-diligence / KYB dossier from the official registry record. |
| `prospect-list` | Building a ranked list of target companies and the people to contact there. |

## Sign-in

On first use Claude opens the Global Database sign-in page. Sign in with your Global
Database account, or create a free account there with your work email and a 6-digit code.
Nothing is configured in the client and Claude never sees your password.

A Global Database account is required. A free tier is available; sustained use requires a
paid plan from Global Database.

## Install in Claude Code

```
/plugin marketplace add global-database/mcp-server
/plugin install global-database@global-database
```

## Privacy Policy

The plugin itself stores no data. Requests go to the Global Database MCP server, governed
by the privacy policy at https://mcp.globaldatabase.com/static/privacy.html. Conversation
content is never stored or used to train models.

## Support

support@globaldatabase.com · https://github.com/global-database/mcp-server

## License

MIT for the plugin files in this folder (skills, manifests, documentation). The hosted
server and the Global Database API are proprietary and governed by
https://mcp.globaldatabase.com/static/terms.html.
