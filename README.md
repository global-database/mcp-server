# Global Database — MCP Server

[![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=global-database&config=eyJ0eXBlIjogImh0dHAiLCAidXJsIjogImh0dHBzOi8vbWNwLmdsb2JhbGRhdGFiYXNlLmNvbS9tY3AifQ==)
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_server-0098FF?logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=global-database&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fmcp.globaldatabase.com%2Fmcp%22%7D)
[![Smithery](https://img.shields.io/badge/Smithery-global--database-7c3aed)](https://smithery.ai/servers/global-database)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-com.globaldatabase%2Fmcp-1f6feb)](https://registry.modelcontextprotocol.io)

Remote [MCP](https://modelcontextprotocol.io/) server that gives LLM agents access to
[Global Database](https://globaldatabase.com/): company profiles, financials, ownership,
digital insights, people search and contact enrichment, prospecting, and KYB/compliance
lookups against official government registries.

Hosted at **`https://mcp.globaldatabase.com/mcp`** (Streamable HTTP). Nothing to install
or run — you connect to it and sign in with your Global Database API key through the
browser.

## Install

### Cursor

Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (per project):

```json
{
  "mcpServers": {
    "global-database": {
      "type": "http",
      "url": "https://mcp.globaldatabase.com/mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http global-database https://mcp.globaldatabase.com/mcp
```

Or install the plugin, which adds the server **and** the `company-due-diligence` skill:

```
/plugin marketplace add global-database/mcp-server
/plugin install global-database@global-database
```

### VS Code (GitHub Copilot)

Use the **Install server** badge above, or add it from the terminal:

```bash
code --add-mcp '{"name":"global-database","type":"http","url":"https://mcp.globaldatabase.com/mcp"}'
```

### Gemini CLI

Install the bundled extension straight from this repo:

```bash
gemini extensions install https://github.com/global-database/mcp-server
```

Or add the server to `settings.json` by hand:

```json
{
  "mcpServers": {
    "global-database": {
      "httpUrl": "https://mcp.globaldatabase.com/mcp",
      "authProviderType": "dynamic_discovery"
    }
  }
}
```

### Perplexity

Requires a paid plan (custom connectors are a Pro/Enterprise feature). In **Settings →
Connectors → + Custom connector → Remote**, enter:

| Field | Value |
|---|---|
| Name | Global Database |
| MCP Server URL | `https://mcp.globaldatabase.com/mcp` |
| Authentication | OAuth |
| Transport | Streamable HTTP |

Then open the connector card to run the OAuth sign-in.

### Grok

At [grok.com/connectors](https://grok.com/connectors) → **New Connector → Custom**, enter the
MCP server URL `https://mcp.globaldatabase.com/mcp` and complete the OAuth sign-in. Grok
discovers the tools from the live endpoint.

### Microsoft Copilot Studio

In your agent → **Tools → Add a tool → Model Context Protocol → New MCP server**, enter the
server URL `https://mcp.globaldatabase.com/mcp` and pick **OAuth 2.0** with dynamic
registration / discovery. Leave **Scope empty** — the server publishes no scopes, and a
non-empty one fails the token request.

Copilot Studio ignores the MCP `instructions` field, so the agent starts without the routing
rules every other client receives. Paste
[`copilot-studio-instructions.md`](copilot-studio-instructions.md) into **Agent → Overview →
Instructions** after the connection is created.

### Claude.ai / other MCP clients

Add a custom connector pointing at `https://mcp.globaldatabase.com/mcp`.

## Authentication

OAuth 2.1 with PKCE and Dynamic Client Registration — the client registers itself, so there
is nothing to configure. On first connect your browser opens a Global Database login page
where you paste your API key; the key is held in the access-token claims server-side and is
never passed as a tool argument.

Get an API key at [globaldatabase.com](https://globaldatabase.com/).

## Tools

| Tool | What it does |
|---|---|
| `check_api_key` | Verify the API connection and return current user info. |
| `get_company_by_website` | Look up a company by website URL or domain. |
| `get_company_by_linkedin` | Look up a company by LinkedIn URL or public ID. |
| `get_company_by_identifiers` | Look up a company by name, registration number, VAT, ticker, website, email, or LinkedIn. |
| `get_company_details` | Full company profile by `company_id`. |
| `get_company_financials` | Balance sheet, ratios, and key metrics per year. |
| `get_company_ownership` | Shareholders and corporate group structure. |
| `get_digital_insights` | Web traffic, rankings, traffic sources, WHOIS, technologies. |
| `search_employees` | Find the people at a company, or people by name, role, department, or seniority. |
| `get_employee_details` | Full profile for one person from a `search_employees` row. |
| `find_people_by_domain` | Find people at companies given by web domain, via the contact-enrichment providers. |
| `enrich_employee_contacts` | Find and enrich one named employee/contact — email, phone, socials. |
| `get_nomenclature` | Lookup values for use with prospecting filters. |
| `prospecting` | Search and filter companies by country, industry, size, revenue, and more. |
| `kyb_search` | Search official government registries for KYB/compliance checks. |
| `kyb_company_details` | Official registry details for a company. |
| `kyb_officers` | Directors, secretaries, and officers from the official registry. |
| `kyb_shareholders` | Shareholders from the official registry. |
| `kyb_shareholders_search` | Reverse shareholder lookup by holder name, across jurisdictions. |
| `kyb_group_structure` | Corporate group structure from the official registry. |
| `kyb_financial` | Detailed financial statements across multiple years. |
| `kyb_officers_search` | Reverse officer lookup by person's name, across jurisdictions. |

## Resources and prompts

Beyond tools, the server exposes MCP resources so a client can load reference data once per
conversation instead of spending a tool call (and credits) on it:

| Resource | Contents |
|---|---|
| `gdb://nomenclature/country` | Country list for the `prospecting` location filter. |
| `gdb://nomenclature/kyb-countries` | Country list for `kyb_search`. |
| `gdb://nomenclature/company-status` | Company status values for `prospecting`. |
| `gdb://nomenclature/department` | Department ids for `search_employees`. |
| `gdb://nomenclature/seniority` | Seniority ids for `search_employees`. |
| `gdb://docs/prospecting-filters` | Full prospecting filter catalog — field names and value formats. |
| `gdb://docs/intent-glossary` | Keyword → tool glossary for routing a request. |

Larger, hierarchical nomenclatures (NACE, ISIC, SIC, industry focus, region) stay behind the
`get_nomenclature` tool and its `search` parameter.

Prompts shipped with the server: `company_research`, `due_diligence`, `lead_generation`,
`competitor_analysis`, `market_research`.

## Plugins and skill

The same contents ship as a plugin for both Cursor (`.cursor-plugin/plugin.json`) and
Claude Code (`.claude-plugin/marketplace.json`), so the server can be installed from a
marketplace instead of being wired up by hand. Each plugin bundles:

- the remote MCP server above (all tools), and
- a **`company-due-diligence`** skill that walks the agent through a structured KYB
  review — resolve the entity, then pull registry details, officers, shareholders,
  group structure and financials into one dossier.

## Where it is listed

| Registry | Entry |
|---|---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io) | `com.globaldatabase/mcp` — published from [`server.json`](server.json) |
| [Smithery](https://smithery.ai/servers/global-database) | `global-database` (verified) |
| Claude Code plugins | `/plugin marketplace add global-database/mcp-server` |
| Cursor marketplace | `global-database` |
| Gemini CLI extensions | `gemini extensions install https://github.com/global-database/mcp-server` |

Maintainer notes — publishing, DNS verification and the remaining directories:
[`PUBLISHING.md`](PUBLISHING.md).

## Links

- [Homepage](https://mcp.globaldatabase.com)
- [Smithery listing](https://smithery.ai/servers/global-database)
- [Privacy policy](https://mcp.globaldatabase.com/static/privacy.html)
- [Terms](https://mcp.globaldatabase.com/static/terms.html)

## About this repository

Distribution metadata only (`server.json`, `.mcp.json`, `plugin.json`,
`.claude-plugin/`, `.cursor-plugin/`, `gemini-extension.json`) so MCP directories and
clients can discover the hosted server, plus the client-side extras that ship with it — the
`company-due-diligence` skill and the Copilot Studio instruction block. MIT covers this
metadata; the server implementation and the Global Database API are not open source.
