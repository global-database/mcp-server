import * as vscode from 'vscode';

/**
 * Registers the Global Database MCP server with VS Code's agent mode.
 *
 * The server is remote and hosted by us, so there is nothing to install, spawn or
 * configure. The provider hands VS Code a URL; VS Code performs the OAuth
 * authorization-code flow against the server's advertised metadata and stores the
 * tokens itself. No API key is ever written into settings.
 */

const PROVIDER_ID = 'globalDatabaseProvider';
const SERVER_LABEL = 'Global Database';
const SERVER_URL = 'https://mcp.globaldatabase.com/mcp';

export function activate(context: vscode.ExtensionContext) {
    const didChangeEmitter = new vscode.EventEmitter<void>();

    const version = context.extension.packageJSON?.version as string | undefined;

    context.subscriptions.push(
        vscode.lm.registerMcpServerDefinitionProvider(PROVIDER_ID, {
            onDidChangeMcpServerDefinitions: didChangeEmitter.event,

            provideMcpServerDefinitions: async () => {
                // Positional constructor: (label, uri, headers?, version?). The
                // published guide shows an options object; the shipped API does not
                // take one, and passing it fails to compile.
                return [
                    new vscode.McpHttpServerDefinition(
                        SERVER_LABEL,
                        vscode.Uri.parse(SERVER_URL),
                        {},
                        version
                    ),
                ];
            },

            // Called when the server is about to start. Nothing to resolve: the server
            // advertises its own authorization metadata and VS Code drives the browser
            // OAuth flow from there. Kept explicit rather than omitted, because this is
            // where credential prompting would go if the transport ever changed.
            resolveMcpServerDefinition: async (server: vscode.McpServerDefinition) => server,
        })
    );

    context.subscriptions.push(didChangeEmitter);
}

export function deactivate() {}
