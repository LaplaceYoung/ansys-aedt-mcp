# agents.md

Current project goal:

Build a Python MCP server that automates Ansys Electronics Desktop through PyAEDT and AEDT native APIs. The server should expose broad control over sessions, projects, variables, modeling, setup, simulation, reports, charts, exports, and generic AEDT/PyAEDT calls.

Project constraints:

- Prefer `uv` for dependency and command execution.
- Keep the implementation modular and testable without a local AEDT license.
- Use PyAEDT as the primary API surface.
- Use AEDT native COM/gRPC objects through PyAEDT as a fallback for functions beyond dedicated wrappers.
- Add focused tests for logic that can run without AEDT.

Verification:

- Run `uv run pytest` for local logic.
- Run `uv run ruff check .` for static checks.
- Real AEDT smoke tests require Windows with a licensed AEDT installation.
