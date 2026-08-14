# Publishing and listing

Where this server is (or can be) listed, and what each channel needs from this repo.

Most directories — Glama, PulseMCP, mcp.so, awesome-mcp-servers clones, and a growing set
of clients — either scrape the [official MCP Registry](https://registry.modelcontextprotocol.io)
or scrape GitHub. Getting the registry entry right and keeping the repo metadata clean
covers the majority of them; the rest are per-channel forms.

## 1. Official MCP Registry (highest leverage)

Manifest: [`server.json`](server.json) — schema `2025-12-11`, remote `streamable-http`.

The `com.globaldatabase/mcp` name is a reverse-DNS namespace, so publishing needs **DNS
authentication** on `globaldatabase.com` (the alternative, `io.github.global-database/mcp`,
uses GitHub OAuth instead and needs no DNS record, but reads as a personal namespace).

### One-time: DNS key

```bash
MY_DOMAIN="globaldatabase.com"

# macOS: system openssl is LibreSSL and cannot do Ed25519 — use openssl@3
# (brew install openssl@3; /opt/homebrew/opt/openssl@3/bin/openssl)
openssl genpkey -algorithm Ed25519 -out key.pem

PUBLIC_KEY="$(openssl pkey -in key.pem -pubout -outform DER | tail -c 32 | base64)"
echo "${MY_DOMAIN}. IN TXT \"v=MCPv1; k=ed25519; p=${PUBLIC_KEY}\""
```

Add that TXT record on the **apex** of `globaldatabase.com` — not under a `_mcp-auth`
selector, which the registry does not read. Keep `key.pem` out of this repo.

### Publish

```bash
brew install mcp-publisher   # or the release tarball

PRIVATE_KEY="$(openssl pkey -in key.pem -noout -text | grep -A3 "priv:" | tail -n +2 | tr -d ' :\n')"
mcp-publisher login dns --domain globaldatabase.com --private-key "${PRIVATE_KEY}"
mcp-publisher publish
```

CI does the same on a version tag — [`.github/workflows/publish-mcp.yml`](.github/workflows/publish-mcp.yml).
It expects the private key in the `MCP_PRIVATE_KEY` secret of a protected
`mcp-registry-publish` environment. Each publish needs a new `version`; the workflow takes
it from the tag.

Verify:

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers/com.globaldatabase%2Fmcp/versions/latest" | jq
```

## 2. GitHub repo metadata

Directories that scrape GitHub rank on description, topics, licence and README. Set them
once:

```bash
gh repo edit global-database/mcp-server \
  --description "Remote MCP server for Global Database — company profiles, financials, ownership, people search, prospecting and KYB/compliance lookups." \
  --homepage "https://mcp.globaldatabase.com" \
  --add-topic mcp --add-topic mcp-server --add-topic model-context-protocol \
  --add-topic claude --add-topic company-data --add-topic kyb \
  --add-topic prospecting --add-topic enrichment --add-topic b2b-data
```

`LICENSE` (MIT, metadata only) is already in the repo — GitHub's licence detection and
several directory filters depend on it.

## 3. Per-client packaging already in this repo

| Channel | File | Notes |
|---|---|---|
| Claude Code plugin marketplace | `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json` | `/plugin marketplace add global-database/mcp-server` |
| Cursor plugin marketplace | `.cursor-plugin/plugin.json`, `mcp.json` | Submitted through Cursor's marketplace form. |
| Gemini CLI extension | `gemini-extension.json` | `gemini extensions install <repo url>` |
| Generic MCP config | `.mcp.json`, `mcp.json` | Read by Claude Code, Cursor and most clients. |
| Smithery | `smithery.yaml` (server repo) | Listed as `global-database`. |
| Microsoft Copilot Studio | `copilot-studio-instructions.md` | Connector setup lives in the server repo. |

## 4. Directories that need a manual submission

| Directory | How |
|---|---|
| [Glama](https://glama.ai/mcp/servers) | "Add server" form; it then tracks the GitHub repo. |
| [PulseMCP](https://www.pulsemcp.com/) | Submission form; also ingests the official registry. |
| [mcp.so](https://mcp.so/) | Submission form. |
| [Smithery](https://smithery.ai/) | Already listed and verified. |
| [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Pull request. |
| Docker MCP Catalog | PR to `docker/mcp-registry` — remote servers are accepted. |

## 5. Release checklist

1. Bump `version` in `server.json`, `plugin.json`, `.cursor-plugin/plugin.json`,
   `.claude-plugin/*.json`, `gemini-extension.json` — keep them identical.
2. Update the tool table in `README.md` if tools changed.
3. Tag: `git tag v0.2.0 && git push origin v0.2.0` → the workflow publishes to the registry.
4. Confirm the registry entry with the `curl` above.
