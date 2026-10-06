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
| Claude Code plugin marketplace | `.claude-plugin/marketplace.json`, `plugins/global-database/` (the plugin itself) | `/plugin marketplace add global-database/mcp-server` |
| Cursor plugin marketplace | `.cursor-plugin/plugin.json`, `mcp.json` | Submitted through Cursor's marketplace form. |
| Gemini CLI extension | `gemini-extension.json` | `gemini extensions install <repo url>` |
| Generic MCP config | `.mcp.json`, `mcp.json` | Read by Claude Code, Cursor and most clients. |
| Smithery | `smithery.yaml` (server repo) | Listed as `global-database`. |
| Microsoft Copilot Studio | `copilot-studio-instructions.md` | Connector setup lives in the server repo. |

## 4. Directories — state as of 2026-09-01

Each row below was checked against the live site on that date, not inferred.

**Done, nothing to submit:**

| Directory | Note |
|---|---|
| [Smithery](https://smithery.ai/servers/global-database) | Listed. |
| [Glama](https://glama.ai/mcp/connectors/com.globaldatabase/mcp) | Listed, and it does ingest the official registry — the entry carries our `server.json` description verbatim. **Listed twice**: a second entry sits at `com.globaldatabase.mcp/global-database` from an older manual submission. Claim the registry-derived one (GitHub, HTTP challenge, or DNS — we already hold the DNS key) and ask support@glama.ai to drop the other. Claiming the duplicate instead is the wrong way round: the registry-derived entry regenerates no matter how often it is deleted. |
| [Claude Connectors Directory](https://claude.ai/directory/global-database) | Listed at **Community** tier. Two follow-ups: request verification, and refresh the tool list — it advertises five tools against the twenty-three the server registers, and two of the five (`get_company_by_url`, `autocomplete`) are Python function names from before the `@mcp.tool(name=...)` rename, so the snapshot predates it. |
| [OpenAI ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_696f807d21a481918a1ed1f43d719ce9) | Listed since 2026-06-23. |
| [Cursor Directory](https://cursor.directory/plugins/mcp-global-database-3) | Listed. **Also twice** — `plugins/global-database-1` is the duplicate. |
| [mcptop.com](https://mcptop.com/server/openai-global-database) | Third-party leaderboard; ingests automatically, no submission exists. |
| [Claude Plugin Directory](https://claude.com/plugins) | **Submitted 2026-09-01, pending review.** A different directory from the Connectors one above — it lists a *plugin* (`plugins/global-database/`: the MCP server plus `skills/`), installable in Claude Code and Cowork. Filed through <https://platform.claude.com/plugins/submit>; the Console form requires an **Admin** role on the organisation, a Developer cannot file it. The review pipeline pins a commit SHA, so push before submitting. |

**Open:**

| Directory | State |
|---|---|
| [PulseMCP](https://www.pulsemcp.com/submit) | **Cannot submit.** The form is closed: "we are not accepting new MCP server or client submissions, and we are not making changes to existing listings", and it points at the Official MCP Registry as the thing to do instead — which is done. They say they will pick it up when their pipeline reopens. The banner still reads "until mid-August" well past that date, so treat the restart as unscheduled. |
| [mcp.so](https://mcp.so/submit?type=remote-server) | **Paid — $39** for a remote-server listing. A spend decision, not a packaging task. |
| VS Code / GitHub MCP gallery | **Not an ingest of the official registry**, contrary to what this file used to imply. `code.visualstudio.com/mcp` redirects to <https://github.com/mcp>, served by `api.mcp.github.com` — a different service from `registry.modelcontextprotocol.io`. Paginating its whole catalogue returned 250 servers across three pages, none of them ours. It is curated; the route in is not documented publicly and has not been found. |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | **No longer accepts third-party entries.** Its README now says the repo holds only the steering group's reference servers and directs readers to the MCP Registry — where we already are. Treat this one as satisfied elsewhere, not outstanding. |
| [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Pull request. Not attempted. |
| Docker MCP Catalog | PR to `docker/mcp-registry`; remote servers are accepted. Not attempted. |
| Perplexity — curated connector catalog | **No self-serve submission exists.** Confirmed 2026-09-11 against the Help Center and two open threads on `community.perplexity.ai` asking the same question with no official answer beyond "use the custom connector." The custom-connector route (per-user, self-serve, already live) is documented in `README.md`. Curated-catalog entries seen in the wild (Semrush, PitchBook "Essential Partner", Canary Data) are negotiated business partnerships, not technical submissions — contact is `partnerships@perplexity.ai`. Not attempted. |
| Microsoft Copilot Studio — MCP server certification | Submitted 2026-09-11, in progress. Internal notes (Partner Center IDs, Key Vault, credentials) kept locally, not in this repo. |

## 4b. Visual Studio Marketplace — the VS Code route that is actually open

Separate from the gallery row above, and worth keeping straight. `github.com/mcp` is a
curated catalogue with no submission route. **Visual Studio Marketplace is self-serve**, and
the way an MCP server reaches it is wrapped in an extension: `vscode-extension/` in this
repo is that wrapper.

It contributes `mcpServerDefinitionProviders` in `package.json` and implements
`vscode.lm.registerMcpServerDefinitionProvider`, handing VS Code the remote URL. Nothing is
spawned locally and no API key is stored — VS Code drives the OAuth flow against the
server's own metadata. Precedents on the Marketplace: Microsoft's Azure MCP Server and the
PostgreSQL extension.

**One correction worth keeping.** The published guide at
<https://code.visualstudio.com/api/extension-guides/ai/mcp> shows
`new vscode.McpHttpServerDefinition({ label, uri, version })` — an options object. The
shipped API does not accept one; it is positional,
`constructor(label: string, uri: Uri, headers?, version?)`, and the documented form fails to
compile with `TS2554: Expected 2-4 arguments, but got 1`. Build against `@types/vscode`
rather than the guide.

Publishing, once a publisher account exists on Azure DevOps:

```bash
cd vscode-extension
npm install
npx @vscode/vsce package --no-dependencies   # produces the .vsix, verified
npx @vscode/vsce publish                     # needs a Personal Access Token
```

Keep `vscode-extension/package.json` `version` in step with the other manifests — it is an
eighth place the version is declared, and `scripts/check_manifests.py` already checks it
(`check_versions` and `check_vscode_extension`).

## 5. Release checklist

1. Bump `version` in `server.json`, `plugin.json`, `.cursor-plugin/plugin.json`,
   `.claude-plugin/*.json`, `gemini-extension.json` — keep them identical.
2. Update the tool table in `README.md` if tools changed.
3. Validate **both** manifests. `claude plugin validate <path> --strict` picks one target,
   and `.claude-plugin/marketplace.json` wins when it exists — so that command alone never
   checks `plugin.json`. To cover it, copy the repo to a temp directory, delete
   `marketplace.json` from the copy, and validate that. Both must pass.
4. Tag: `git tag v0.2.1 && git push origin v0.2.1` → the workflow publishes to the registry.
   The registry is append-only on versions: a published version cannot be replaced with
   different content, only superseded, so a mistake is fixed by bumping again.
   `description` is capped at **100 characters** by the registry schema — the long product
   copy belongs in the per-client manifests, not here.
5. Confirm the registry entry with the `curl` above.
