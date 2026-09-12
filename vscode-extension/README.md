# Global Database for VS Code

Company intelligence and KYB data from official government registries, available to
VS Code agent mode as an MCP server.

Installing this extension registers the server. There is nothing to configure: the
server is remote and hosted by Global Database, and the extension hands VS Code a URL
rather than spawning a process.

## What it adds

23 read-only tools, grouped:

| Area | What you can ask for |
|---|---|
| Entity resolution | Resolve a company from a website, LinkedIn URL, name, registration number, VAT number or ticker |
| Company | Firmographic profile, filed financials, ownership and corporate group structure, digital footprint |
| KYB | Official-registry record, directors and officers, shareholders, group structure, filed statements — searchable by company or by person |
| People | Employee search, individual profiles, contact enrichment |
| Prospecting | Filtered company search across firmographic criteria |

Coverage: 400+ government registries, 600M+ companies, 195+ countries. Every value
traces back to an official source.

## Sign-in

The first request opens a browser OAuth flow. Sign in with a Global Database account
and VS Code stores the tokens. **No API key goes into your settings or into any file in
your repository.**

An account is required. See <https://globaldatabase.com/>.

## Without this extension

The same server can be added by hand — the extension exists to remove the step, not to
enable something otherwise impossible:

```json
// .vscode/mcp.json
{
  "servers": {
    "global-database": {
      "type": "http",
      "url": "https://mcp.globaldatabase.com/mcp"
    }
  }
}
```

## Links

- [Homepage](https://mcp.globaldatabase.com)
- [Source and other clients](https://github.com/global-database/mcp-server)
- [Privacy policy](https://www.globaldatabase.com/privacy-policy)
