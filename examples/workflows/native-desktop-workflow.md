# Desktop and Native AEDT Workflow

This workflow uses the Desktop app plus native AEDT module calls. It is useful for environments where Desktop automation is available and solver-specific app constructors require additional license features.

```text
aedt_environment
aedt_start_session(app_name="desktop", version="2024.2", non_graphical=true)
aedt_new_project(project_name="MCPNativeProject")
aedt_insert_design(design_type="HFSS", design_name="HFSSDesign1", solution_type="DrivenModal")
aedt_set_active_project(project_name="MCPNativeProject")
aedt_set_active_design(design_name="HFSSDesign1", design_type="HFSS")
aedt_native_module_call(module_name="AnalysisSetup", method="GetSetups")
aedt_native_get_properties(target="oproject", tab="ProjectVariableTab", server="ProjectVariables")
aedt_native_change_property(target="oproject", change_payload=["NAME:AllTabs"])
aedt_call(target="omodule", module_name="ReportSetup", method="GetAllReportNames")
aedt_save_project(project_path="outputs/native-desktop-demo.aedt")
aedt_release_session(close_projects=true, close_desktop=true)
```

Use `aedt_list_api(target="omodule", module_name="...")` to inspect available native module methods before building larger native workflows.

