# Examples

These workflows show practical MCP call sequences for common AEDT automation tasks. They are written as tool-call plans so they can be adapted to Claude Desktop, Codex MCP clients, MCP Inspector, or any client that can call `ansys-aedt-mcp`.

## Workflows

- [HFSS S-parameter workflow](workflows/hfss-sparameter-workflow.md)
- [Icepak thermal workflow](workflows/icepak-thermal-workflow.md)
- [Desktop/native AEDT workflow](workflows/native-desktop-workflow.md)

## Local Prerequisites

- Windows with Ansys Electronics Desktop installed.
- `uv sync --extra dev`
- `uv run ansys-aedt-mcp`
- Solver licenses for workflows that instantiate solver apps directly.

