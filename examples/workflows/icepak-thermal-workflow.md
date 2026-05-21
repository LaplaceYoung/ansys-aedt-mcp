# Icepak Thermal Workflow

This workflow outlines an Icepak thermal automation path for block creation, material assignment, thermal sources, monitors, solve control, monitor data, and summary export.

```text
aedt_environment
aedt_start_session(app_name="icepak", version="2024.2", non_graphical=true)
aedt_set_variable(name="power", expression="3W")
aedt_create_geometry(primitive="box", args=[[0, 0, 0], ["20mm", "20mm", "3mm"]], kwargs={"name": "IC"})
aedt_assign_material(assignment="IC", material="silicon")
aedt_icepak_operation(method="assign_source", args=["IC", "Total Power", "power"])
aedt_icepak_operation(method="assign_point_monitor", args=[[0, 0, "5mm"]], kwargs={"monitor_name": "TopMonitor"})
aedt_create_setup(name="Setup1", properties={"Flow Regime": "Laminar"})
aedt_validate_design(validation_kind="simple")
aedt_analyze_setup(name="Setup1", cores=8, blocking=true)
aedt_get_monitor_data
aedt_export_icepak_summary(output_dir="outputs", solution_name="Setup1", quantity="Temperature", filename="icepak-summary")
aedt_save_project(project_path="outputs/icepak-thermal-demo.aedt")
```

`aedt_icepak_operation` covers common thermal sources, openings, walls, monitors, fans, network objects, and mesh generation helpers.

