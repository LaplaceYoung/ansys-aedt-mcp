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
| Environment/API discovery | `aedt_environment`, `aedt_api_manifest` | Python/PyAEDT availability, supported app names, constructors, and public method signatures |
| Session | `aedt_start_session`, `aedt_release_session`, `aedt_session_info` | Launch/connect to major AEDT apps |
| Project | `aedt_open_project`, `aedt_save_project`, `aedt_list_projects`, `aedt_new_project`, `aedt_insert_design`, `aedt_set_active_project`, `aedt_set_active_design`, `aedt_design_summary` | Load, save, list, create projects, insert native designs, activate context, and summarize designs |
| Variables | `aedt_set_variable`, `aedt_get_variables` | Project/design variable management |
| Datasets/import | `aedt_create_dataset`, `aedt_import_dataset`, `aedt_import_cad` | AEDT design/project datasets and CAD/layout import |
| Modeling | `aedt_create_geometry`, `aedt_modeler_summary`, `aedt_modeler_operation`, `aedt_assign_material`, `aedt_materials_summary`, `aedt_materials_operation`, `aedt_material_object_summary`, `aedt_mesh_operation`, `aedt_mesh_summary`, `aedt_call(target="modeler")` | Common primitives, modeler summaries, transforms, booleans, sweeps, coordinate systems, material assignment, material library operations, object material property summaries, mesh operation summaries, mesh operations, and full modeler bridge |
| Setup/sweeps | `aedt_create_setup`, `aedt_setup_summary`, `aedt_get_setup_properties`, `aedt_update_setup`, `aedt_create_frequency_sweep`, `aedt_create_open_region`, `aedt_call(target="app")` | Setup creation, setup introspection, setup property updates, frequency sweeps, and open-region setup |
| Boundaries/excitations | `aedt_assign_boundary_or_excitation`, `aedt_create_port`, `aedt_source_port_summary`, `aedt_native_module_call`, `aedt_call(target="omodule")` | Dedicated assignment dispatch, ports/sources, and native AEDT module control |
| Solver-specific controls | `aedt_hfss_operation`, `aedt_maxwell_operation`, `aedt_q3d_operation`, `aedt_icepak_operation`, `aedt_circuit_operation` | Allowlisted HFSS boundaries/sources/scattering, Maxwell windings/motion/forces, Q3D nets/matrices, Icepak thermal controls, and Circuit schematic/source operations |
| Simulation | `aedt_analyze`, `aedt_analyze_setup`, `aedt_solve_in_batch`, `aedt_apply_solved_variation`, `aedt_validate_design`, `aedt_cleanup_solution`, `aedt_list_variations` | Analyze setup or active design, run batch solves, apply solved variations, validate designs, clean solution data, and list variations |
| Optimetrics | `aedt_create_parametric_sweep`, `aedt_create_optimization`, `aedt_optimetrics_summary`, `aedt_parametric_operation`, `aedt_optimization_operation`, `aedt_optimetrics_setup_operation`, `aedt_call(target="parametrics")`, `aedt_call(target="optimizations")` | Parametric sweeps, optimization, sensitivity/statistical/DOE flows, setup import/delete/update/calculation controls, and generic optimization bridge |
| Reports | `aedt_create_output_variable`, `aedt_get_output_variable`, `aedt_get_evaluated_value`, `aedt_get_nominal_variation`, `aedt_get_profile`, `aedt_create_report`, `aedt_create_field_plot`, `aedt_get_solution_data`, `aedt_get_traces_for_plot`, `aedt_get_touchstone_data`, `aedt_get_monitor_data`, `aedt_post_summary`, `aedt_post_operation`, `aedt_insert_near_field`, `aedt_export_report`, `aedt_export_field_plot`, `aedt_export_diagnostics`, `aedt_export_matrix_data`, `aedt_export_icepak_summary`, `aedt_export_app_data` | Output variables, expression evaluation, nominal variations, profile data, report creation, field plots, post-processing summaries, report operations, field exports, plot operations, trace discovery, Touchstone data, monitor data, near-field definitions, matrix data, Icepak summaries, diagnostics, and exports |
| Deletion | `aedt_delete_item` | Controlled deletion of setups, variables, projects, and designs |
| Project/design maintenance | `aedt_change_design_settings`, `aedt_change_validation_settings`, `aedt_read_design_data`, `aedt_project_design_operation` | Design settings, validation settings, design data reads, and allowlisted project/design operations |
| Configuration | `aedt_configuration_summary`, `aedt_configuration_operation`, `aedt_update_configuration_options` | Configuration import/export and export/import option management |
| Native/OO properties | `aedt_native_get_properties`, `aedt_native_get_property_value`, `aedt_native_change_property`, `aedt_oo_object_names`, `aedt_oo_get_properties`, `aedt_oo_get_property_value`, `aedt_oo_set_property_value` | AEDT `GetProperties`, `GetPropertyValue`, `ChangeProperty`, and PyAEDT object-oriented property tree control |
| Broad API/workflows | `aedt_list_api`, `aedt_call`, `aedt_batch_call`, `aedt_run_app_method` | Public PyAEDT/native AEDT method access and ordered multi-step execution |

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
- MCP server currently registers 94 tools.
- `uv run pyaedt --json aedt-versions` detects AEDT `2024.2` at `G:\ANSYSEM2024\AnsysEM\v242\Win64`.
- `aedt_start_session(app_name="desktop", version="2024.2", non_graphical=True)` launches and releases AEDT Desktop successfully.
- `aedt_new_project(project_name="MCPNativeProject")` creates and lists a native AEDT project successfully.
- Solver app constructors such as `Hfss(...)` timed out in this local AEDT 2024 R2 environment during smoke testing. Desktop/native mode remains the verified path for this machine, and app-specific tools remain available for environments where solver app construction succeeds.
