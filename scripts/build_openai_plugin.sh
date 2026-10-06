#!/usr/bin/env bash
# Build the ChatGPT plugin package: the ZIP uploaded at platform.openai.com ->
# Plugins -> Global Database -> "Upload plugin to make changes".
#
# OpenAI wants the agent-plugins layout (plugin.json with extensions.com.openai at the
# root), which is not the plugin.json the other channels read from this repo's root.
# So the OpenAI manifest lives in openai-plugin/, and the skills and logo are copied in
# from the repo root at build time -- one copy of each skill, shared by every channel.
#
# The package declares NO MCP server -- no mcp.json, no apps/.app.json. The plugin keeps
# the server ChatGPT already has (MCPs tab, "Configured"); the ZIP only carries metadata
# and skills. Both ways of naming the server failed on 2026-10-05:
#   - .app.json (apps -> asdk_app_696f...) uploads, but blocks Submit for review:
#     "Plugins with .app.json cannot be submitted. Declare an MCP server URL instead."
#   - mcp.json with the same URL is refused at upload: "Adding, removing, or replacing an
#     MCP server isn't supported for existing plugins."
# supportURL is still required in the interface block, the plugin having an MCP server.
#
# `name` in openai-plugin/plugin.json is "app-696f...", not "global-database": the portal
# refuses an upload whose name differs from the package ChatGPT already holds.
#
# The package version is its own: ChatGPT had 1.0.0 live before this repo's 0.2.x line
# existed. Bump openai-plugin/plugin.json for every upload.
#
#     scripts/build_openai_plugin.sh   ->  dist/global-database-openai-<version>.zip
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" "$REPO/openai-plugin/plugin.json")"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

cp "$REPO/openai-plugin/plugin.json" "$STAGE/"
cp -R "$REPO/plugins/global-database/skills" "$STAGE/skills"
mkdir -p "$STAGE/assets"
cp "$REPO/logo.png" "$STAGE/assets/logo.png"
find "$STAGE" -name .DS_Store -delete

mkdir -p "$REPO/dist"
OUT="$REPO/dist/global-database-openai-$VERSION.zip"
rm -f "$OUT"
(cd "$STAGE" && zip -qr "$OUT" .)
echo "$OUT"
unzip -l "$OUT"
