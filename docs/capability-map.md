# AEDT MCP Capability Map

## Source Basis

- MCP Python SDK supports `FastMCP`, structured tool outputs, stdio execution, and streamable HTTP transports.
- PyAEDT provides Python application classes for Desktop, HFSS, Q3D, Q2D, Maxwell 2D/3D, Icepak, HFSS 3D Layout, Mechanical, RMxprt, Circuit, Maxwell Circuit, EMIT, and Twin Builder.
- PyAEDT VariableManager handles project variables prefixed with `$`, design variables, dependent variables, independent variables, and expression evaluation.
- PyAEDT Optimetrics exposes `parametrics` and `optimizations`.
- PyAEDT post-processing exposes report classes, field plots, report creation, and solution data extraction.
- PyAEDT exposes native AEDT handles including `odesktop`, `oproject`, `odesign`, `oeditor`, and `odesign.GetModule(...)` for AEDT Client Library coverage.

## Implemented Tool Surface

| Area | Tools | Coverage |
| --- | --- | --- |
| Environment | `aedt_environment` | Python/PyAEDT availability and supported app names |
| Session | `aedt_start_session`, `aedt_release_session`, `aedt_session_info` | Launch/connect to major AEDT apps |
| Project | `aedt_open_project`, `aedt_save_project`, `aedt_list_projects`, `aedt_new_project`, `aedt_insert_design` | Load, save, list, create projects, and insert native designs |
| Variables | `aedt_set_variable`, `aedt_get_variables` | Project/design variable management |
| Datasets | `aedt_create_dataset`, `aedt_import_dataset` | AEDT design and project datasets |
| Modeling | `aedt_create_geometry`, `aedt_assign_material`, `aedt_call(target="modeler")` | Common primitives, material assignment, and full modeler bridge |
| Setup | `aedt_create_setup`, `aedt_call(target="app")` | Setup creation and property updates |
| Simulation | `aedt_analyze` | Analyze setup or active design |
| Optimetrics | `aedt_create_parametric_sweep`, `aedt_create_optimization`, `aedt_call(target="parametrics")`, `aedt_call(target="optimizations")` | Parametric sweeps, optimization, sensitivity/statistical/DOE flows, and generic optimization bridge |
| Reports | `aedt_create_report`, `aedt_create_field_plot`, `aedt_get_solution_data`, `aedt_export_report`, `aedt_export_field_plot`, `aedt_export_app_data` | Report creation, field plots, data access, and exports |
| Broad API | `aedt_list_api`, `aedt_call`, `aedt_run_app_method` | Public PyAEDT and native AEDT method access |

## Native AEDT Bridge Targets

- `odesktop`: Desktop-level AEDT object.
- `oproject`: active project object.
- `odesign`: active design object.
- `oeditor`: active editor/modeler object.
- `omodule`: any module returned by `odesign.GetModule(module_name)`, such as `Optimetrics`, `BoundarySetup`, `AnalysisSetup`, `ReportSetup`, or solver-specific modules.

## Verification Tiers

1. Local logic: unit tests with fake AEDT objects.
2. Dependency/import: `uv run ansys-aedt-mcp --help` and `aedt_environment` through MCP Inspector.
3. AEDT smoke: launch a non-graphical app session on a licensed Windows machine.
4. End-to-end workflow: create variables, geometry, setup, sweep, analyze, report, and export CSV from a sample project.

## Current Local Evidence

- `uv sync --extra dev` succeeds with Python 3.12.10, `mcp 1.27.1`, and `pyaedt 0.27.1`.
- `uv run pyaedt --json aedt-versions` detects AEDT `2024.2` at `G:\ANSYSEM2024\AnsysEM\v242\Win64`.
- `aedt_start_session(app_name="desktop", version="2024.2", non_graphical=True)` launches and releases AEDT Desktop successfully.
- `aedt_new_project(project_name="MCPNativeProject")` creates and lists a native AEDT project successfully.
- Solver app constructors such as `Hfss(...)` timed out in this local AEDT 2024 R2 environment during smoke testing. Desktop/native mode remains the verified path for this machine, and app-specific tools remain available for environments where solver app construction succeeds.
