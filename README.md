# Global Database — MCP Server

[![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=global-database&config=eyJ0eXBlIjogImh0dHAiLCAidXJsIjogImh0dHBzOi8vbWNwLmdsb2JhbGRhdGFiYXNlLmNvbS9tY3AifQ==)
[![smithery badge](https://smithery.ai/badge/global-database)](https://smithery.ai/servers/global-database)

Remote [MCP](https://modelcontextprotocol.io/) server that gives LLM agents access to
[Global Database](https://globaldatabase.com/): company profiles, financials, ownership,
digital insights, contact enrichment, prospecting, and KYB/compliance lookups against
official government registries.

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
| `enrich_employee_contacts` | Find and enrich an employee/contact. |
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

## Cursor plugin

This repo is also packaged as a Cursor plugin (`.cursor-plugin/plugin.json` + `mcp.json`),
so it can be installed from the Cursor marketplace, not only wired up by hand. It bundles:

- the remote MCP server above (all tools), and
- a **`company-due-diligence`** skill that walks the agent through a structured KYB
  review — resolve the entity, then pull registry details, officers, shareholders,
  group structure and financials into one dossier.

## Links

- [Homepage](https://mcp.globaldatabase.com)
- [Smithery listing](https://smithery.ai/servers/global-database)
- [Privacy policy](https://mcp.globaldatabase.com/static/privacy.html)
- [Terms](https://mcp.globaldatabase.com/static/terms.html)

## About this repository

Distribution metadata only (`.mcp.json`, `plugin.json`) so MCP directories can discover the
hosted server. The server implementation is not open source.
