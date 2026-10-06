"""Check the distribution manifests against each other and against reality.

This repository ships one product to a dozen consumers, each wanting its own manifest
format. No single file can tell you the others still agree with it, and every failure
mode here is silent: a directory serves a stale version, a listing points at a URL that
started 404ing months ago, or a config loads without error and connects to nothing.

    python3 scripts/check_manifests.py [--offline]

Each check below corresponds to a defect that was actually present at some point.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMA_URL = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"

# Every place a version is declared, as (file, key path). Absent from this list means
# the file carries no version — say so on purpose, do not let it drift by omission.
#
# openai-plugin/plugin.json is left out on purpose: the ChatGPT package has its own
# version line (1.0.0 was live there before this repo's 0.2.x existed), bumped per upload
# by scripts/build_openai_plugin.sh's caller.
VERSIONED = [
    ("server.json", ("version",)),
    ("plugin.json", ("version",)),
    ("gemini-extension.json", ("version",)),
    (".cursor-plugin/plugin.json", ("version",)),
    (".claude-plugin/plugin.json", ("version",)),
    (".claude-plugin/marketplace.json", ("version",)),
    (".claude-plugin/marketplace.json", ("plugins", 0, "version")),
    ("vscode-extension/package.json", ("version",)),
]

# The same endpoint, under the key each client insists on. Copying the wrong file
# between clients produces a config that loads and connects to nothing, which is how
# Antigravity stayed broken for weeks.
SERVER_KEY_BY_FILE = {
    ".mcp.json": ("mcpServers", "url"),
    "mcp.json": ("mcpServers", "url"),
    ".vscode/mcp.json": ("servers", "url"),
    "gemini-extension.json": ("mcpServers", "httpUrl"),
}

EXPECTED_URL = "https://mcp.globaldatabase.com/mcp"

URLS = [
    "https://mcp.globaldatabase.com",
    "https://mcp.globaldatabase.com/mcp",
    "https://mcp.globaldatabase.com/static/logo.png",
    "https://www.globaldatabase.com/privacy-policy",
    "https://mcp.globaldatabase.com/.well-known/oauth-authorization-server",
    "https://smithery.ai/servers/global-database",
    "https://claude.ai/directory/global-database",
]

# `/mcp` answers 401 until a token is presented. That is the correct response to an
# unauthenticated probe, not a fault.
ACCEPTABLE = {200, 401}


def _load(relative: str):
    return json.loads((REPO / relative).read_text(encoding="utf-8"))


def _fetch(url: str, timeout: int = 15):
    request = urllib.request.Request(url, headers={"User-Agent": "gdb-manifest-check"})
    return urllib.request.urlopen(request, timeout=timeout)


def check_server_json_schema(problems, notes, offline):
    if offline:
        print("server.json     skipped (offline)")
        return
    server = _load("server.json")
    try:
        schema = json.loads(_fetch(SCHEMA_URL).read().decode("utf-8"))
    except urllib.error.URLError as exc:
        problems.append(f"could not fetch the registry schema: {exc}")
        return
    try:
        import jsonschema
    except ImportError:
        notes.append("jsonschema is not installed, so server.json was not validated")
        return
    try:
        jsonschema.validate(server, schema)
    except jsonschema.ValidationError as exc:
        where = "/".join(str(p) for p in exc.absolute_path) or "(root)"
        problems.append(f"server.json fails the registry schema at {where}: {exc.message}")
        return
    print(f"server.json     valid against {SCHEMA_URL.rsplit('/', 2)[1]}")


def check_versions(problems):
    found = {}
    for relative, path in VERSIONED:
        if not (REPO / relative).exists():
            problems.append(f"{relative} is listed as versioned but does not exist")
            continue
        document = _load(relative)
        try:
            for key in path:
                document = document[key]
        except (KeyError, IndexError, TypeError):
            problems.append(f"{relative} has no version at {'.'.join(map(str, path))}")
            continue
        found[f"{relative}:{'.'.join(map(str, path))}"] = document

    distinct = set(found.values())
    if len(distinct) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in sorted(found.items()))
        problems.append(f"manifests declare different versions: {detail}")
    elif distinct:
        print(f"versions        {distinct.pop()} across {len(found)} declarations")


def check_server_keys(problems):
    """Every client config must name the same endpoint under the key that client wants."""
    checked = 0
    before = len(problems)
    for relative, (container_key, url_key) in SERVER_KEY_BY_FILE.items():
        path = REPO / relative
        if not path.exists():
            continue
        document = _load(relative)
        servers = document.get(container_key)
        if servers is None:
            problems.append(
                f"{relative} has no {container_key!r} key — this client will read nothing"
            )
            continue
        for name, entry in servers.items():
            if url_key not in entry:
                problems.append(
                    f"{relative} server {name!r} has no {url_key!r}; keys present: "
                    f"{sorted(entry)}. This loads without error and connects to nothing."
                )
                continue
            if entry[url_key] != EXPECTED_URL:
                problems.append(
                    f"{relative} server {name!r} points at {entry[url_key]}, expected {EXPECTED_URL}"
                )
                continue
            checked += 1
    if len(problems) == before:
        print(f"client configs  {checked} entr(y/ies) name the endpoint under the right key")


def check_vscode_extension(problems):
    relative = "vscode-extension/package.json"
    if not (REPO / relative).exists():
        return
    before = len(problems)
    pkg = _load(relative)

    providers = pkg.get("contributes", {}).get("mcpServerDefinitionProviders")
    if not providers:
        problems.append(f"{relative} declares no contributes.mcpServerDefinitionProviders")
    else:
        declared = {p.get("id") for p in providers}
        source = (REPO / "vscode-extension/src/extension.ts").read_text(encoding="utf-8")
        for provider_id in declared:
            if provider_id and provider_id not in source:
                problems.append(
                    f"{relative} declares provider id {provider_id!r} but extension.ts "
                    "never registers it; VS Code will contribute nothing"
                )

    if not pkg.get("publisher"):
        problems.append(f"{relative} has no publisher; vsce cannot publish it")
    if not pkg.get("engines", {}).get("vscode"):
        problems.append(f"{relative} declares no engines.vscode")

    if len(problems) == before:
        print("vscode ext      provider id matches the registration in extension.ts")


def check_urls(problems, offline):
    if offline:
        print("urls            skipped (offline)")
        return
    for url in URLS:
        try:
            status = _fetch(url).status
        except urllib.error.HTTPError as exc:
            status = exc.code
        except urllib.error.URLError as exc:
            problems.append(f"{url} is unreachable: {exc.reason}")
            continue
        if status not in ACCEPTABLE:
            problems.append(f"{url} returned {status}")
    print(f"urls            {len(URLS)} checked")


def note_gemini(notes):
    """Not a failure — a standing decision this repo has not made.

    Gemini CLI was retired on 18 June 2026 in favour of Antigravity CLI, which rejects
    this manifest's keys. The file still ships here, and the other working copy of this
    repository deleted it and added `antigravity/` instead. Both cannot be right.
    """
    if (REPO / "gemini-extension.json").exists() and not (REPO / "antigravity").exists():
        notes.append(
            "gemini-extension.json ships, but Gemini CLI was retired on 2026-06-18 and "
            "its successor Antigravity requires `serverUrl`, which this file does not "
            "use. There is no antigravity/ directory here. Decide whether to drop the "
            "Gemini manifest and add the Antigravity one — see PUBLISHING.md."
        )


def main() -> int:
    offline = "--offline" in sys.argv
    problems: list[str] = []
    notes: list[str] = []

    check_server_json_schema(problems, notes, offline)
    check_versions(problems)
    check_server_keys(problems)
    check_vscode_extension(problems)
    note_gemini(notes)
    check_urls(problems, offline)

    if notes:
        print(f"\n{len(notes)} note(s):")
        for note in notes:
            print(f"  ! {note}")

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print("\nmanifests agree with each other and with the live endpoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
