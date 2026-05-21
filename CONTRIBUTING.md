# Contributing

Thank you for improving `ansys-aedt-mcp`.

## Contribution Areas

- Solver workflows for HFSS, Maxwell, Q3D, Icepak, Circuit, Twin Builder, EMIT, RMxprt, Mechanical, and HFSS 3D Layout.
- PyAEDT wrapper tools with tests.
- Native AEDT module recipes through `odesign.GetModule(...)`.
- Documentation, examples, prompts, and smoke scripts.
- Bug reports with AEDT version, PyAEDT version, transport mode, and license context.

## Development

```powershell
uv sync --extra dev
uv run ruff check .
uv run pytest
```

## Pull Request Checklist

- Keep changes scoped and reversible.
- Add or update tests for behavior that can run without AEDT.
- Document AEDT-dependent behavior in `docs/verification.md`.
- Include the exact AEDT version, PyAEDT version, and command output for real AEDT smoke tests.
- Keep commercial-use discussions out of implementation PRs; use a separate licensing discussion.

## Style

- Prefer dedicated tools for common workflows.
- Preserve `aedt_call` and native targets for broad AEDT API coverage.
- Serialize AEDT calls through the session manager.
- Keep error messages actionable for MCP clients.
