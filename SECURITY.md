# Security Policy

## Supported Versions

The `main` branch receives security fixes.

## Reporting

Report security issues through a private GitHub security advisory when available. Include:

- Affected version or commit.
- MCP transport in use.
- Minimal reproduction steps.
- AEDT/PyAEDT version context.
- Impact and suggested mitigation.

## Scope

Security-sensitive areas:

- Generic method invocation through `aedt_call`.
- Local file exports and report paths.
- Remote AEDT gRPC connections.
- MCP transport exposure on network interfaces.
- Native AEDT object access through `odesktop`, `oproject`, `odesign`, `oeditor`, and `omodule`.

## Hardening Guidance

- Run streamable HTTP behind trusted network boundaries.
- Prefer stdio transport for local desktop use.
- Keep `allow_private=false` for `aedt_call` unless you control the client and workflow.
- Use dedicated service accounts for shared automation machines.
- Review generated AEDT scripts and exports before sharing artifacts.
