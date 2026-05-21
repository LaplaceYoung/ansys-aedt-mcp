# Q3D Net Workflow

This workflow outlines a Q3D automation path for net assignment, setup creation, net inspection, matrix export, and project save.

```text
aedt_environment
aedt_start_session(app_name="q3d", version="2024.2", non_graphical=true)
aedt_create_geometry(primitive="box", args=[[0, 0, 0], ["20mm", "2mm", "0.5mm"]], kwargs={"name": "Trace"})
aedt_assign_material(assignment="Trace", material="copper")
aedt_q3d_operation(method="assign_net", args=[["Trace"]], kwargs={"net_name": "Signal1", "net_type": "Signal"})
aedt_q3d_net_summary(net_name="Signal1")
aedt_create_setup(name="Setup1")
aedt_analyze_setup(name="Setup1", cores=8, blocking=true)
aedt_export_matrix_data(export_kind="q3d", args=["outputs/q3d-matrix.csv"], kwargs={"setup": "Setup1"})
aedt_save_project(project_path="outputs/q3d-net-demo.aedt")
```

Use `aedt_q3d_net_summary` to inspect sources, sinks, and objects for a selected net before matrix extraction.
