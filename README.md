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
- **Simulation workflow tools:** variables, datasets, geometry, materials, setup inspection/update, sweeps, optimizations, analysis, reports, field plots, diagnostics, Touchstone data, monitors, and exports.
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
| Environment/API discovery | `aedt_environment`, `aedt_api_manifest` |
| Session | `aedt_start_session`, `aedt_release_session`, `aedt_session_info` |
| Project/design | `aedt_open_project`, `aedt_save_project`, `aedt_list_projects`, `aedt_new_project`, `aedt_insert_design`, `aedt_set_active_project`, `aedt_set_active_design`, `aedt_design_summary` |
| Variables/datasets | `aedt_set_variable`, `aedt_get_variables`, `aedt_create_dataset`, `aedt_import_dataset` |
| Modeling/materials | `aedt_create_geometry`, `aedt_modeler_summary`, `aedt_modeler_operation`, `aedt_assign_material`, `aedt_materials_summary`, `aedt_materials_operation`, `aedt_material_object_summary`, `aedt_mesh_operation`, `aedt_mesh_summary`, `aedt_import_cad` |
| Ports/sources | `aedt_create_port`, `aedt_source_port_summary`, `aedt_assign_boundary_or_excitation` |
| Solver-specific controls | `aedt_hfss_operation`, `aedt_maxwell_operation`, `aedt_q3d_operation`, `aedt_icepak_operation`, `aedt_circuit_operation` |
| Simulation | `aedt_create_setup`, `aedt_setup_summary`, `aedt_get_setup_properties`, `aedt_update_setup`, `aedt_create_frequency_sweep`, `aedt_create_open_region`, `aedt_analyze`, `aedt_analyze_setup`, `aedt_solve_in_batch`, `aedt_apply_solved_variation`, `aedt_validate_design`, `aedt_cleanup_solution`, `aedt_list_variations` |
| Exploration | `aedt_create_parametric_sweep`, `aedt_create_optimization`, `aedt_optimetrics_summary`, `aedt_parametric_operation`, `aedt_optimization_operation`, `aedt_optimetrics_setup_operation` |
| Post-processing | `aedt_create_output_variable`, `aedt_get_output_variable`, `aedt_get_evaluated_value`, `aedt_get_nominal_variation`, `aedt_get_profile`, `aedt_create_report`, `aedt_create_field_plot`, `aedt_get_solution_data`, `aedt_get_traces_for_plot`, `aedt_get_touchstone_data`, `aedt_get_monitor_data`, `aedt_post_summary`, `aedt_post_operation`, `aedt_insert_near_field` |
| Export | `aedt_export_report`, `aedt_export_field_plot`, `aedt_export_diagnostics`, `aedt_export_matrix_data`, `aedt_export_icepak_summary`, `aedt_export_app_data` |
| Deletion | `aedt_delete_item` |
| Project/design maintenance | `aedt_change_design_settings`, `aedt_change_validation_settings`, `aedt_read_design_data`, `aedt_project_design_operation` |
| Configuration | `aedt_configuration_summary`, `aedt_configuration_operation`, `aedt_update_configuration_options` |
| Native properties | `aedt_native_get_properties`, `aedt_native_get_property_value`, `aedt_native_change_property` |
| Broad API/workflows | `aedt_run_app_method`, `aedt_list_api`, `aedt_call`, `aedt_batch_call` |

Current MCP registration: **90 tools**.

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
aedt_modeler_operation(method="move", args=[["Box1"], ["1mm", "0mm", "0mm"]])
aedt_assign_material(assignment="Box1", material="copper")
aedt_materials_summary
aedt_materials_operation(method="add_material", args=["demo_material"], kwargs={"properties": {"permittivity": 3.2}})
aedt_create_port(method="wave_port", args=["Face1"], kwargs={"name": "P1"})
aedt_hfss_operation(method="create_scattering", kwargs={"ports": ["P1"]})
aedt_create_setup(name="Setup1")
aedt_update_setup(name="Setup1", properties={"MaximumPasses": 8})
aedt_create_frequency_sweep(sweep_kind="linear_count", args=["Setup1", "GHz", 1, 10])
aedt_create_parametric_sweep(variable="w", start="5mm", stop="20mm", step="5mm")
aedt_optimetrics_summary
aedt_optimetrics_setup_operation(collection="parametrics", setup_name="Parametric1", method="update", kwargs={"update_dictionary": {"SaveFields": true}})
aedt_analyze_setup(name="Setup1", cores=8, blocking=true)
aedt_create_output_variable(variable="s11", expression="dB(S(1,1))")
aedt_get_evaluated_value(name="w", units="mm")
aedt_create_report(expressions="dB(S(1,1))")
aedt_post_summary
aedt_post_operation(method="export_report_to_jpg", args=["outputs", "S11"], kwargs={"width": 1200})
aedt_get_traces_for_plot(kwargs={"setup": "Setup1"})
aedt_get_touchstone_data(setup="Setup1")
aedt_export_report(report_name="S11", output_path="outputs")
aedt_export_diagnostics(export_kind="convergence", setup="Setup1")
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
- `pytest`: 35 passing tests
- MCP tools registered: 90
- Desktop/native AEDT smoke: passing on AEDT 2024 R2

## Documentation

- [Capability map](docs/capability-map.md)
- [Examples](examples/README.md)
- [Client configuration](docs/client-config.md)
- [Verification log](docs/verification.md)
- [Roadmap](docs/roadmap.md)

## Roadmap

- Add solver-license-backed end-to-end HFSS smoke examples.
- Add canonical templates for HFSS, Maxwell 3D, Q3D, Icepak, and Circuit workflows.
- Add MCP prompts for common AEDT modeling and post-processing tasks.
- Add solver-specific templates around diagnostics, near-field extraction, Touchstone analysis, and monitor data.
- Add generated API maps for PyAEDT modeler, post, modules, and native AEDT module names.

## Community

Contributions are welcome for examples, solver-specific wrappers, docs, tests, and verified workflows. Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

This project uses [PolyForm Noncommercial License 1.0.0](LICENSE.md).

Commercial licensing and redistribution permissions require a separate written agreement.
