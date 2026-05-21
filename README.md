<div align="center">

<img src="assets/logo/ansys-aedt-mcp-logo.png" alt="Ansys AEDT MCP Server logo" width="180">

# Ansys AEDT MCP Server

**A Model Context Protocol server for Ansys Electronics Desktop, PyAEDT, HFSS, Maxwell, Q3D, Icepak, Circuit, reports, sweeps, and simulation automation.**

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-compatible-6f42c1)](https://modelcontextprotocol.io/)
[![PyAEDT](https://img.shields.io/badge/PyAEDT-0.26%2B-1793D1)](https://aedt.docs.pyansys.com/)
[![AEDT](https://img.shields.io/badge/Ansys%20Electronics%20Desktop-2024R2%2B-ffb71b)](https://www.ansys.com/products/electronics)
[![License](https://img.shields.io/badge/license-PolyForm--Noncommercial--1.0.0-blue)](LICENSE.md)

[English](README.md) · [简体中文](README.zh-CN.md) · [Documentation](docs/capability-map.md) · [Verification](docs/verification.md)

</div>

## Why This Exists

`ansys-aedt-mcp` lets AI agents and MCP clients control Ansys Electronics Desktop through a structured server interface. It combines dedicated tools for common electromagnetic simulation workflows with a broad PyAEDT/native AEDT bridge for advanced automation.

SEO keywords: Ansys MCP, AEDT MCP server, Ansys Electronics Desktop automation, PyAEDT MCP, HFSS automation, Maxwell automation, Q3D automation, Icepak automation, AI simulation agent, electromagnetic simulation automation, EDA agent tools, CAE automation.

## Highlights

- **MCP-ready:** stdio, SSE, and streamable HTTP transports through the official Python MCP SDK.
- **PyAEDT-first:** HFSS, Maxwell, Q3D/Q2D, Icepak, Circuit, Twin Builder, EMIT, RMxprt, Mechanical, and HFSS 3D Layout entry points.
- **Native AEDT bridge:** `odesktop`, `oproject`, `odesign`, `oeditor`, and `odesign.GetModule(...)` access through controlled tools.
- **Simulation workflow tools:** variables, datasets, geometry, materials, setups, sweeps, optimizations, analysis, reports, field plots, and exports.
- **Agent-safe verification:** unit tests run without AEDT licenses; Desktop/native smoke tests run on licensed Windows AEDT installations.
- **Non-commercial source availability:** research, education, personal experimentation, and public knowledge use under PolyForm Noncommercial 1.0.0.

## Quick Start

```powershell
git clone https://github.com/LaplaceYoung/ansys-aedt-mcp.git
cd ansys-aedt-mcp
uv sync --extra dev
uv run ansys-aedt-mcp
```

Use the MCP inspector during development:

```powershell
uv run mcp dev src/ansysmcp/server.py
```

Run streamable HTTP:

```powershell
uv run ansys-aedt-mcp --transport streamable-http
```

## MCP Client Config

```json
{
  "mcpServers": {
    "ansys-aedt": {
      "command": "uv",
      "args": ["--directory", "F:\\实验\\ansysmcp", "run", "ansys-aedt-mcp"]
    }
  }
}
```

After cloning from GitHub, replace the local path with your checkout path.

## Tool Surface

| Area | Tools |
| --- | --- |
| Environment | `aedt_environment` |
| Session | `aedt_start_session`, `aedt_release_session`, `aedt_session_info` |
| Project/design | `aedt_open_project`, `aedt_save_project`, `aedt_list_projects`, `aedt_new_project`, `aedt_insert_design` |
| Variables/datasets | `aedt_set_variable`, `aedt_get_variables`, `aedt_create_dataset`, `aedt_import_dataset` |
| Modeling/materials | `aedt_create_geometry`, `aedt_assign_material` |
| Simulation | `aedt_create_setup`, `aedt_analyze` |
| Exploration | `aedt_create_parametric_sweep`, `aedt_create_optimization` |
| Post-processing | `aedt_create_report`, `aedt_create_field_plot`, `aedt_get_solution_data` |
| Export | `aedt_export_report`, `aedt_export_field_plot`, `aedt_export_app_data` |
| Broad API | `aedt_run_app_method`, `aedt_list_api`, `aedt_call` |

Current MCP registration: **28 tools**.

## Example Workflows

Desktop/native workflow:

```text
aedt_environment
aedt_start_session(app_name="desktop", version="2024.2", non_graphical=true)
aedt_new_project(project_name="MCPNativeProject")
aedt_insert_design(design_type="HFSS", design_name="HFSSDesign1", solution_type="DrivenModal")
aedt_call(target="omodule", module_name="AnalysisSetup", method="...")
```

PyAEDT solver workflow:

```text
aedt_start_session(app_name="hfss", version="2024.2", non_graphical=true)
aedt_set_variable(name="w", expression="10mm")
aedt_create_geometry(primitive="box", args=[[0, 0, 0], ["w", "5mm", "1mm"]])
aedt_assign_material(assignment="Box1", material="copper")
aedt_create_setup(name="Setup1")
aedt_create_parametric_sweep(variable="w", start="5mm", stop="20mm", step="5mm")
aedt_analyze(setup_name="Setup1")
aedt_create_report(expressions="dB(S(1,1))")
aedt_export_report(report_name="S11", output_path="outputs")
```

## AEDT Requirements

- Windows with Ansys Electronics Desktop installed for real AEDT execution.
- PyAEDT-compatible AEDT version. Local verification detected AEDT `2024.2`.
- Solver-specific licenses for solver app constructors and analysis workflows.
- Python 3.10+; the repository pins local development to Python 3.12 through `.python-version`.

## Verification

```powershell
uv sync --extra dev
uv run ruff check .
uv run pytest
uv run ansys-aedt-mcp --help
uv run python scripts/aedt_smoke.py --mode environment
uv run python scripts/aedt_smoke.py --mode desktop --version 2024.2 --create-project MCPNativeProject
```

Current local status:

- `ruff check`: passing
- `pytest`: 13 passing tests
- MCP tools registered: 28
- Desktop/native AEDT smoke: passing on AEDT 2024 R2

## Documentation

- [Capability map](docs/capability-map.md)
- [Client configuration](docs/client-config.md)
- [Verification log](docs/verification.md)
- [Roadmap](docs/roadmap.md)

## Roadmap

- Add solver-license-backed end-to-end HFSS smoke examples.
- Add canonical templates for HFSS, Maxwell 3D, Q3D, Icepak, and Circuit workflows.
- Add MCP prompts for common AEDT modeling and post-processing tasks.
- Add optional artifact exporters for reports, images, Touchstone, convergence, profiles, and mesh stats.
- Add generated API maps for PyAEDT modeler, post, modules, and native AEDT module names.

## Community

Contributions are welcome for examples, solver-specific wrappers, docs, tests, and verified workflows. Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

This project uses [PolyForm Noncommercial License 1.0.0](LICENSE.md).

Commercial licensing and redistribution permissions require a separate written agreement.
