# HFSS S-Parameter Workflow

This workflow creates a compact HFSS automation path for geometry, variables, ports, setup control, report traces, Touchstone data, and diagnostics.

```text
aedt_environment
aedt_start_session(app_name="hfss", version="2024.2", non_graphical=true)
aedt_set_variable(name="w", expression="10mm")
aedt_set_variable(name="l", expression="40mm")
aedt_create_geometry(primitive="box", args=[[0, 0, 0], ["l", "w", "1mm"]], kwargs={"name": "Trace"})
aedt_modeler_summary
aedt_modeler_operation(method="move", args=[["Trace"], ["1mm", "0mm", "0mm"]])
aedt_assign_material(assignment="Trace", material="copper")
aedt_materials_summary
aedt_create_port(method="wave_port", args=["Face1"], kwargs={"name": "P1"})
aedt_hfss_operation(method="create_scattering", kwargs={"ports": ["P1"]})
aedt_create_setup(name="Setup1", properties={"Frequency": "10GHz", "MaximumPasses": 8})
aedt_create_frequency_sweep(sweep_kind="linear_count", args=["Setup1", "GHz", 1, 10])
aedt_validate_design(validation_kind="simple")
aedt_analyze_setup(name="Setup1", cores=8, blocking=true)
aedt_create_output_variable(variable="s11_db", expression="dB(S(1,1))")
aedt_create_report(expressions="dB(S(1,1))", report_name="S11")
aedt_post_summary
aedt_post_operation(method="export_report_to_jpg", args=["outputs", "S11"], kwargs={"width": 1200})
aedt_get_traces_for_plot(kwargs={"setup": "Setup1"})
aedt_get_touchstone_data(setup="Setup1")
aedt_export_report(report_name="S11", output_path="outputs")
aedt_export_diagnostics(export_kind="convergence", setup="Setup1", output_file="outputs/convergence.csv")
aedt_save_project(project_path="outputs/hfss-sparameter-demo.aedt")
```

For low-level HFSS calls, use `aedt_hfss_operation` for allowlisted boundary/source/network methods and `aedt_call(target="app", method="...")` for long-tail PyAEDT APIs.
