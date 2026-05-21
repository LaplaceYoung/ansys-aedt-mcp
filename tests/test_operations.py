from __future__ import annotations

import pytest

from ansysmcp.operations import (
    analyze_setup,
    apply_solved_variation,
    assign_boundary_or_excitation,
    assign_material,
    batch_call,
    change_design_settings,
    change_validation_settings,
    circuit_operation,
    cleanup_solution,
    configuration_operation,
    configuration_summary,
    create_dataset,
    create_field_plot,
    create_frequency_sweep,
    create_open_region,
    create_optimization,
    create_output_variable,
    create_port,
    delete_item,
    design_summary,
    export_app_data,
    export_diagnostics,
    export_icepak_summary,
    export_matrix_data,
    get_evaluated_value,
    get_monitor_data,
    get_nominal_variation,
    get_output_variable,
    get_profile,
    get_setup_properties,
    get_touchstone_data,
    get_traces_for_plot,
    hfss_operation,
    icepak_operation,
    import_cad,
    import_dataset,
    insert_design,
    insert_near_field,
    invoke,
    list_api,
    list_projects,
    list_variations,
    material_object_summary,
    materials_operation,
    materials_summary,
    maxwell_operation,
    mesh_operation,
    modeler_operation,
    modeler_summary,
    native_change_property,
    native_get_properties,
    native_get_property_value,
    native_module_call,
    new_project,
    post_operation,
    post_summary,
    project_design_operation,
    q3d_operation,
    read_design_data,
    set_active_design,
    set_active_project,
    set_variable,
    setup_summary,
    solve_in_batch,
    source_port_summary,
    update_configuration_options,
    update_setup,
    validate_design,
)
from ansysmcp.session import (
    AedtError,
    AedtSessionManager,
    AedtSessionState,
    api_manifest,
    normalize_app_name,
)


class DummyVariableManager:
    def __init__(self) -> None:
        self.calls = []
        self.variables = {"width": DummyVariable("10mm")}
        self.variable_names = ["width"]
        self.design_variable_names = ["width"]
        self.project_variable_names = []

    def set_variable(self, name: str, expression: str, description: str | None = None) -> bool:
        self.calls.append((name, expression, description))
        self.variables[name] = DummyVariable(expression)
        return True

    def get_expression(self, name: str) -> str:
        return self.variables[name].expression


class DummyVariable:
    def __init__(self, expression: str) -> None:
        self.expression = expression


class DummyModeler:
    def __init__(self) -> None:
        self.created = []
        self.model_units = "mm"
        self.object_names = ["Box1", "Box2"]
        self.solid_names = ["Box1", "Box2"]
        self.sheet_names = ["Sheet1"]
        self.line_names = ["Line1"]
        self.coordinate_systems = ["Global"]

    def create_box(self, position, dimensions, name=None, matname=None):
        self.created.append((position, dimensions, name, matname))
        return {"name": name, "material": matname}

    def get_model_bounding_box(self):
        return [0, 0, 0, 10, 20, 30]

    def get_line_ids(self):
        return {"Line1": 1}

    def move(self, assignment, vector):
        return {"assignment": assignment, "vector": vector}

    def unite(self, assignment, purge=False, keep_originals=False):
        return {"assignment": assignment, "purge": purge, "keep_originals": keep_originals}


class DummyOptimizations:
    def add(self, calculation=None, ranges=None, variables=None, optimization_type="Optimization"):
        return {
            "calculation": calculation,
            "ranges": ranges,
            "variables": variables,
            "optimization_type": optimization_type,
        }


class DummyPost:
    all_report_names = ["S11"]
    available_report_types = ["Rectangular Plot"]
    field_plot_names = ["EField"]
    post_solution_type = "DrivenModal"
    update_report_dynamically = True

    def create_fieldplot_surface(
        self,
        assignment,
        quantity,
        setup=None,
        intrinsics=None,
        plot_name=None,
        field_type="DC R/L Fields",
    ):
        return {
            "kind": "surface",
            "assignment": assignment,
            "quantity": quantity,
            "setup": setup,
            "intrinsics": intrinsics,
            "plot_name": plot_name,
            "field_type": field_type,
        }

    def available_report_solutions(self, report_category=None):
        return ["Setup1 : Sweep1"]

    def get_all_report_quantities(self, solution=None, context=None, is_siwave_dc=False):
        return {"S Parameter": ["dB(S(1,1))"]}

    def rename_report(self, plot_name, new_name):
        return {"plot_name": plot_name, "new_name": new_name}

    def export_report_to_jpg(
        self,
        project_path,
        plot_name,
        width=800,
        height=450,
        image_format="jpg",
    ):
        return {
            "project_path": project_path,
            "plot_name": plot_name,
            "width": width,
            "height": height,
            "image_format": image_format,
        }

    def get_scalar_field_value(self, quantity, scalar_function="Maximum", **kwargs):
        return {"quantity": quantity, "scalar_function": scalar_function, **kwargs}


class DummyMesh:
    def assign_length_mesh(self, assignment, maximum_length):
        return {"assignment": assignment, "maximum_length": maximum_length}


class DummyMaterials:
    def __init__(self) -> None:
        self.material_keys = ["copper", "FR4_epoxy"]
        self.surface_material_keys = ["black_paint"]
        self.conductors = ["copper"]
        self.dielectrics = ["FR4_epoxy"]
        self.liquids = ["water"]
        self.gases = ["air"]

    def get_used_project_material_names(self):
        return ["copper"]

    def add_material(self, name, properties=None):
        self.material_keys.append(name)
        return {"name": name, "properties": properties or {}}

    def export_materials_to_file(self, output_file):
        return output_file


class DummyConfigurationOptions:
    def __init__(self) -> None:
        self.export_variables = True
        self.export_materials = True
        self.import_variables = True
        self.skip_import_if_exists = True

    def set_all_export(self):
        self.export_variables = True
        self.export_materials = True
        return True

    def unset_all_import(self):
        self.import_variables = False
        return True


class DummyConfigurations:
    def __init__(self) -> None:
        self.options = DummyConfigurationOptions()

    def export_config(self, config_file=None, overwrite=False):
        return {"config_file": config_file, "overwrite": overwrite}

    def import_config(self, config_file, *args):
        return {"config_file": config_file, "args": args}


class DummySetup:
    def __init__(self, name: str) -> None:
        self.name = name
        self.props = {"MaximumPasses": 6, "BasisOrder": 1}
        self.updated = False

    def update(self) -> bool:
        self.updated = True
        return True


class DummyApp:
    def __init__(self) -> None:
        self.variable_manager = DummyVariableManager()
        self.modeler = DummyModeler()
        self.optimizations = DummyOptimizations()
        self.post = DummyPost()
        self.mesh = DummyMesh()
        self.materials = DummyMaterials()
        self.configurations = DummyConfigurations()
        self.boundaries = ["Boundary1"]
        self.ports = ["P1"]
        self.sources = ["Source1"]
        self.setups = ["Setup1"]
        self.setup_names = ["Setup1"]
        self.setup_sweeps_names = ["Sweep1"]
        self.active_setup = "Setup1"
        self.nominal_sweep = "Setup1 : Sweep1"
        self.setup_objects = {"Setup1": DummySetup("Setup1")}

    def echo(self, value: str) -> str:
        return value

    def analyze_setup(self, name=None, cores=None, tasks=None, blocking=True):
        return {"name": name, "cores": cores, "tasks": tasks, "blocking": blocking}

    def solve_in_batch(self, file_name=None, machine="localhost", cores=4, setup=None):
        return {"file_name": file_name, "machine": machine, "cores": cores, "setup": setup}

    def validate_simple(self, log_file=None):
        return 1 if log_file else 0

    def validate_full_design(self, design=None, output_dir=None, ports=None):
        return [f"design={design}", f"ports={ports}"], True

    def cleanup_solution(self, variations="All", entire_solution=True, field=True, mesh=True):
        return {
            "variations": variations,
            "entire_solution": entire_solution,
            "field": field,
            "mesh": mesh,
        }

    def change_design_settings(self, settings):
        return {"settings": settings}

    def change_validation_settings(
        self,
        entity_check_level="Strict",
        ignore_unclassified=False,
        skip_intersections=False,
    ):
        return {
            "entity_check_level": entity_check_level,
            "ignore_unclassified": ignore_unclassified,
            "skip_intersections": skip_intersections,
        }

    def list_of_variations(self, setup=None, sweep=None):
        return [f"{setup}:{sweep}:w='10mm'"]

    def read_design_data(self):
        return {"design": "HFSSDesign1"}

    def duplicate_design(self, name, save_after_duplicate=True):
        return {"name": name, "save_after_duplicate": save_after_duplicate}

    def apply_solved_variation(self, variation):
        return {"applied": variation}

    def get_nominal_variation(self, with_values=False):
        if with_values:
            return {"w": "10mm"}
        return "w='10mm'"

    def get_evaluated_value(self, name, units=None):
        return {"name": name, "units": units, "value": 10}

    def get_output_variable(self, variable, solution=None):
        return {"variable": variable, "solution": solution, "value": -12.3}

    def get_profile(self, name=None):
        return {"name": name, "passes": 3}

    def assign_material(self, assignment, material):
        return {"assignment": assignment, "material": material}

    def create_dataset(self, **kwargs):
        return kwargs

    def import_dataset1d(self, input_file, name=None, is_project_dataset=True, sort=True):
        return {
            "input_file": input_file,
            "name": name,
            "is_project_dataset": is_project_dataset,
            "sort": sort,
        }

    def export_results(self, export_folder=None):
        return [export_folder]

    def assign_wave_port(self, assignment, name=None):
        return {"assignment": assignment, "name": name}

    def wave_port(self, assignment, name=None):
        return {"assignment": assignment, "name": name}

    def get_all_sources(self):
        return ["Source1"]

    def get_all_source_modes(self):
        return ["Source1:1"]

    def get_all_conductors_names(self):
        return ["copper"]

    def get_all_dielectrics_names(self):
        return ["FR4_epoxy"]

    def get_object_material_properties(self, assignment=None, prop_names=None):
        return {"assignment": assignment, "prop_names": prop_names, "conductivity": "5.8e7"}

    def create_linear_count_sweep(self, setup, unit, start_frequency, stop_frequency):
        return {
            "setup": setup,
            "unit": unit,
            "start_frequency": start_frequency,
            "stop_frequency": stop_frequency,
        }

    def get_setups(self):
        return list(self.setup_objects)

    def get_sweeps(self, setup_name):
        return [f"{setup_name}_Sweep1"]

    def get_setup(self, name):
        return self.setup_objects[name]

    def export_convergence(self, setup, variations="", output_file=None):
        return {"setup": setup, "variations": variations, "output_file": output_file}

    def create_scattering(self, plot="S Parameter Plot Nominal", ports=None):
        return {"plot": plot, "ports": ports}

    def assign_winding(self, assignment=None, name=None, current=1):
        return {"assignment": assignment, "name": name, "current": current}

    def assign_net(self, assignment, net_name=None, net_type="Signal"):
        return {"assignment": assignment, "net_name": net_name, "net_type": net_type}

    def assign_source(self, assignment, thermal_condition, assignment_value):
        return {
            "assignment": assignment,
            "thermal_condition": thermal_condition,
            "assignment_value": assignment_value,
        }

    def create_schematic_from_netlist(self, input_file):
        return {"input_file": input_file}

    def export_matrix_data(self, file_name, setup=None):
        return {"file_name": file_name, "setup": setup}

    def export_summary(self, output_dir=None, solution_name=None, type="Object", **kwargs):
        return {
            "output_dir": output_dir,
            "solution_name": solution_name,
            "type": type,
            **kwargs,
        }

    def create_open_region(self, frequency="1GHz", boundary="Radiation", **kwargs):
        return {"frequency": frequency, "boundary": boundary, **kwargs}

    def create_output_variable(self, variable, expression, solution=None, context=None):
        return {
            "variable": variable,
            "expression": expression,
            "solution": solution,
            "context": context,
        }

    def get_traces_for_plot(self, **kwargs):
        return {"kwargs": kwargs, "traces": ["dB(S(1,1))"]}

    def get_touchstone_data(self, setup=None, sweep=None, variations=None):
        return {"setup": setup, "sweep": sweep, "variations": variations}

    def get_monitor_data(self):
        return [{"name": "Monitor1", "quantity": "Temperature"}]

    def insert_near_field_sphere(self, name, **kwargs):
        return {"name": name, **kwargs}

    def import_3d_cad(self, input_file, **kwargs):
        return {"input_file": input_file, **kwargs}

    def import_dxf(self, input_file, **kwargs):
        return {"input_file": input_file, "kind": "dxf", **kwargs}

    def delete_setup(self, name):
        return {"deleted": name}


class DummyProject:
    def __init__(self, name="Project1") -> None:
        self.name = name
        self.designs = []

    def GetName(self):
        return self.name

    def Rename(self, name, _overwrite):
        self.name = name

    def InsertDesign(self, design_type, design_name, solution_type, _unused):
        self.designs.append((design_type, design_name, solution_type))
        return True

    def GetModule(self, module_name):
        return DummyModule(module_name)

    def GetProperties(self, tab, server):
        return [f"{tab}:{server}:Prop"]

    def GetPropertyValue(self, tab, server, property_name):
        return f"{tab}:{server}:{property_name}:Value"

    def ChangeProperty(self, payload):
        return {"changed": payload}


class DummyModule:
    def __init__(self, module_name) -> None:
        self.module_name = module_name

    def GetSetups(self):
        return ["Setup1"]


class DummyNativeDesktop:
    def __init__(self, desktop) -> None:
        self.desktop = desktop

    def NewProject(self):
        project = DummyProject()
        self.desktop.projects.append(project)
        self.desktop.active = project
        return project


class DummyDesktop:
    def __init__(self) -> None:
        self.projects = []
        self.active = None
        self.odesktop = DummyNativeDesktop(self)

    @property
    def project_list(self):
        return [project.GetName() for project in self.projects]

    @property
    def active_project_name(self):
        return self.active.GetName() if self.active else None

    @property
    def active_design_name(self):
        if self.active and self.active.designs:
            return self.active.designs[-1][1]
        return None

    def active_project(self, name=None):
        if name:
            self.active = next(project for project in self.projects if project.GetName() == name)
        return self.active

    def active_design(self, name=None, design_type=None, project_object=None):
        if name is None:
            return self.active
        if self.active and name:
            self.active.designs.append((design_type, name, ""))
        return {"name": name, "design_type": design_type, "project": project_object}

    def design_list(self, project=None):
        selected = self.active
        if project:
            selected = next(item for item in self.projects if item.GetName() == project)
        if selected is None:
            return []
        return [design[1] for design in selected.designs]


def active_manager() -> AedtSessionManager:
    manager = AedtSessionManager()
    manager._state = AedtSessionState("hfss", DummyApp())
    return manager


def desktop_manager() -> AedtSessionManager:
    manager = AedtSessionManager()
    manager._state = AedtSessionState("desktop", DummyDesktop())
    return manager


def test_normalize_app_name_accepts_alias() -> None:
    assert normalize_app_name("HFSS 3D") == "hfss"
    assert normalize_app_name("Maxwell_3D") == "maxwell3d"


def test_api_manifest_reports_constructor_and_methods() -> None:
    manifest = api_manifest("hfss")
    assert "hfss" in manifest
    assert "constructor" in manifest["hfss"]
    assert "create_setup" in manifest["hfss"]["methods"]


def test_invoke_calls_public_method() -> None:
    app = DummyApp()
    assert invoke(app, method="echo", args=["ok"]) == "ok"


def test_batch_call_executes_ordered_public_calls() -> None:
    manager = active_manager()
    result = batch_call(
        manager,
        operations=[
            {"target": "app", "method": "echo", "args": ["one"]},
            {"target": "app", "method": "assign_material", "args": [["Box1"], "copper"]},
        ],
    )
    assert result["ok"] is True
    assert result["completed"] == 2
    assert result["results"][0]["result"] == "one"
    assert result["results"][1]["result"] == {"assignment": ["Box1"], "material": "copper"}


def test_batch_call_stops_on_error_by_default() -> None:
    manager = active_manager()
    result = batch_call(
        manager,
        operations=[
            {"target": "app", "method": "missing_method"},
            {"target": "app", "method": "echo", "args": ["two"]},
        ],
    )
    assert result["ok"] is False
    assert result["completed"] == 1


def test_invoke_blocks_private_access() -> None:
    app = DummyApp()
    with pytest.raises(AedtError):
        invoke(app, attr_path="__class__")


def test_list_api_splits_methods_and_attributes() -> None:
    api = list_api(DummyApp())
    assert "echo" in api["methods"]
    assert "modeler" in api["attributes"]


def test_set_variable_uses_variable_manager() -> None:
    manager = active_manager()
    result = set_variable(manager, name="width", expression="12mm", description="trace width")
    assert result["result"] is True
    assert manager.app.variable_manager.calls == [("width", "12mm", "trace width")]


def test_assign_material_uses_app_api() -> None:
    result = assign_material(active_manager(), assignment=["Box1"], material="copper")
    assert result["result"] == {"assignment": ["Box1"], "material": "copper"}


def test_modeler_summary_and_operation_use_modeler_api() -> None:
    manager = active_manager()
    summary = modeler_summary(manager)
    moved = modeler_operation(
        manager,
        method="move",
        args=[["Box1"], [1, 2, 3]],
    )
    united = modeler_operation(
        manager,
        method="unite",
        args=[["Box1", "Box2"]],
        kwargs={"keep_originals": True},
    )
    assert summary["model_units"] == "mm"
    assert summary["object_names"] == ["Box1", "Box2"]
    assert summary["get_model_bounding_box"] == [0, 0, 0, 10, 20, 30]
    assert moved["result"]["vector"] == [1, 2, 3]
    assert united["result"]["keep_originals"] is True


def test_materials_and_configuration_wrappers_use_manager_apis() -> None:
    manager = active_manager()
    material_summary = materials_summary(manager)
    material_added = materials_operation(
        manager,
        method="add_material",
        args=["new_dielectric"],
        kwargs={"properties": {"permittivity": 3.2}},
    )
    material_export = materials_operation(
        manager,
        method="export_materials_to_file",
        args=["materials.json"],
    )
    config_summary = configuration_summary(manager)
    config_export = configuration_operation(
        manager,
        method="export_config",
        kwargs={"config_file": "design.json", "overwrite": True},
    )
    config_options = update_configuration_options(
        manager,
        options={"skip_import_if_exists": False},
        action="unset_all_import",
    )
    assert material_summary["conductors"] == ["copper"]
    assert material_summary["used_project_material_names"] == ["copper"]
    assert material_added["result"]["name"] == "new_dielectric"
    assert material_export["result"] == "materials.json"
    assert config_summary["options"]["export_variables"] is True
    assert config_export["result"]["overwrite"] is True
    assert config_options["options"]["import_variables"] is False
    assert config_options["options"]["skip_import_if_exists"] is False


def test_create_and_import_dataset_use_app_api() -> None:
    manager = active_manager()
    created = create_dataset(manager, name="curve", x=[1, 2], y=[3, 4], x_unit="GHz")
    imported = import_dataset(manager, input_file="curve.csv", name="curve")
    assert created["dataset"]["name"] == "curve"
    assert created["dataset"]["x_unit"] == "GHz"
    assert imported["dataset"]["input_file"] == "curve.csv"


def test_create_optimization_uses_optimetrics_api() -> None:
    result = create_optimization(
        active_manager(),
        calculation="dB(S(1,1))",
        ranges={"w": ["1mm", "5mm"]},
        variables=["w"],
    )
    assert result["optimization"]["calculation"] == "dB(S(1,1))"


def test_create_field_plot_dispatches_by_kind() -> None:
    result = create_field_plot(
        active_manager(),
        plot_kind="surface",
        assignment="Box1",
        quantity="Mag_E",
        plot_name="EField",
    )
    assert result["field_plot"]["kind"] == "surface"
    assert result["field_plot"]["plot_name"] == "EField"


def test_post_summary_and_operation_use_post_api() -> None:
    manager = active_manager()
    summary = post_summary(manager)
    renamed = post_operation(
        manager,
        method="rename_report",
        args=["S11", "S11_Renamed"],
    )
    exported = post_operation(
        manager,
        method="export_report_to_jpg",
        args=["outputs", "S11"],
        kwargs={"width": 1200},
    )
    scalar = post_operation(
        manager,
        method="get_scalar_field_value",
        args=["Mag_E"],
        kwargs={"scalar_function": "Maximum", "object_name": "Box1"},
    )
    assert summary["all_report_names"] == ["S11"]
    assert summary["available_report_solutions"] == ["Setup1 : Sweep1"]
    assert renamed["result"]["new_name"] == "S11_Renamed"
    assert exported["result"]["width"] == 1200
    assert scalar["result"]["object_name"] == "Box1"


def test_export_app_data_uses_allowlisted_method() -> None:
    result = export_app_data(
        active_manager(),
        export_kind="results",
        kwargs={"export_folder": "out"},
    )
    assert result["result"] == ["out"]


def test_native_project_tools_use_desktop_api() -> None:
    manager = desktop_manager()
    project = new_project(manager, project_name="MCPNativeProject")
    design = insert_design(
        manager,
        design_type="HFSS",
        design_name="HFSSDesign1",
        solution_type="DrivenModal",
    )
    projects = list_projects(manager)
    assert project["project_name"] == "MCPNativeProject"
    assert design["result"] is True
    assert projects["designs"]["MCPNativeProject"] == ["HFSSDesign1"]


def test_active_project_and_design_tools_use_desktop_api() -> None:
    manager = desktop_manager()
    new_project(manager, project_name="MCPNativeProject")
    project = set_active_project(manager, project_name="MCPNativeProject")
    design = set_active_design(manager, design_name="HFSSDesign1", design_type="HFSS")
    assert project["projects"]["active_project_name"] == "MCPNativeProject"
    assert design["design"]["name"] == "HFSSDesign1"


def test_design_summary_includes_session_and_app_lists() -> None:
    summary = design_summary(active_manager())
    assert summary["session"]["active"] is True
    assert summary["setups"] == ["Setup1"]
    assert summary["boundaries"] == ["Boundary1"]


def test_analysis_control_wrappers_dispatch_to_app() -> None:
    manager = active_manager()
    setup = analyze_setup(manager, name="Setup1", cores=8, tasks=2, blocking=False)
    batch = solve_in_batch(manager, file_name="project.aedt", setup="Setup1", cores=4)
    variation = apply_solved_variation(manager, variation={"w": "10mm"})
    assert setup["result"]["cores"] == 8
    assert setup["result"]["tasks"] == 2
    assert batch["result"]["file_name"] == "project.aedt"
    assert variation["result"]["applied"] == {"w": "10mm"}


def test_design_validation_and_settings_wrappers_dispatch_to_app() -> None:
    manager = active_manager()
    validation = validate_design(
        manager,
        validation_kind="full",
        kwargs={"design": "HFSSDesign1", "ports": 1},
    )
    cleanup = cleanup_solution(manager, variations="w=10mm", mesh=False)
    design_settings = change_design_settings(manager, settings={"SolveMatrixAtLast": True})
    validation_settings = change_validation_settings(
        manager,
        entity_check_level="Warning",
        skip_intersections=True,
    )
    variations = list_variations(manager, setup="Setup1", sweep="Sweep1")
    design_data = read_design_data(manager)
    operation = project_design_operation(
        manager,
        method="duplicate_design",
        args=["Copy1"],
        kwargs={"save_after_duplicate": False},
    )
    assert validation["method"] == "validate_full_design"
    assert validation["result"][1] is True
    assert cleanup["result"]["mesh"] is False
    assert design_settings["result"]["settings"]["SolveMatrixAtLast"] is True
    assert validation_settings["result"]["entity_check_level"] == "Warning"
    assert variations["variations"] == ["Setup1:Sweep1:w='10mm'"]
    assert design_data["design_data"]["design"] == "HFSSDesign1"
    assert operation["result"]["name"] == "Copy1"


def test_value_profile_and_material_summaries_use_app_apis() -> None:
    manager = active_manager()
    nominal = get_nominal_variation(manager, with_values=True)
    evaluated = get_evaluated_value(manager, name="w", units="mm")
    output = get_output_variable(manager, variable="s11", solution="Setup1")
    profile = get_profile(manager, name="Setup1")
    materials = material_object_summary(manager, assignment=["Box1"], prop_names=["conductivity"])
    assert nominal["variation"] == {"w": "10mm"}
    assert evaluated["value"]["units"] == "mm"
    assert output["value"]["value"] == -12.3
    assert profile["profile"]["passes"] == 3
    assert materials["get_all_conductors_names"] == ["copper"]
    assert materials["object_material_properties"]["assignment"] == ["Box1"]


def test_boundary_and_mesh_wrappers_dispatch_to_app_objects() -> None:
    manager = active_manager()
    boundary = assign_boundary_or_excitation(
        manager,
        method="assign_wave_port",
        args=["Face1"],
        kwargs={"name": "P1"},
    )
    mesh = mesh_operation(
        manager,
        method="assign_length_mesh",
        args=["Box1"],
        kwargs={"maximum_length": "1mm"},
    )
    assert boundary["result"] == {"assignment": "Face1", "name": "P1"}
    assert mesh["result"] == {"assignment": "Box1", "maximum_length": "1mm"}


def test_port_and_source_summary_wrappers_dispatch_to_app() -> None:
    manager = active_manager()
    port = create_port(
        manager,
        method="wave_port",
        args=["Face1"],
        kwargs={"name": "P1"},
    )
    summary = source_port_summary(manager)
    assert port["result"] == {"assignment": "Face1", "name": "P1"}
    assert summary["ports"] == ["P1"]
    assert summary["get_all_source_modes"] == ["Source1:1"]


def test_sweep_region_output_import_and_delete_wrappers() -> None:
    manager = active_manager()
    sweep = create_frequency_sweep(
        manager,
        sweep_kind="linear_count",
        args=["Setup1", "GHz", 1, 10],
    )
    region = create_open_region(manager, frequency="2GHz", boundary="Radiation")
    output = create_output_variable(manager, variable="s11", expression="dB(S(1,1))")
    imported = import_cad(manager, input_file="board.dxf")
    deleted = delete_item(manager, method="delete_setup", args=["Setup1"])
    assert sweep["method"] == "create_linear_count_sweep"
    assert region["result"]["frequency"] == "2GHz"
    assert output["result"]["expression"] == "dB(S(1,1))"
    assert imported["method"] == "import_dxf"
    assert deleted["result"] == {"deleted": "Setup1"}


def test_setup_summary_and_update_wrappers_use_setup_api() -> None:
    manager = active_manager()
    summary = setup_summary(manager)
    setup = get_setup_properties(manager, name="Setup1")
    updated = update_setup(manager, name="Setup1", properties={"MaximumPasses": 10})
    assert summary["setup_names"] == ["Setup1"]
    assert summary["sweeps"]["Setup1"] == ["Setup1_Sweep1"]
    assert setup["properties"]["MaximumPasses"] == 6
    assert updated["result"] is True
    assert updated["properties"]["MaximumPasses"] == 10


def test_post_processing_data_wrappers_use_app_api() -> None:
    manager = active_manager()
    traces = get_traces_for_plot(manager, kwargs={"setup": "Setup1"})
    touchstone = get_touchstone_data(manager, setup="Setup1", sweep="Sweep1")
    monitors = get_monitor_data(manager)
    near_field = insert_near_field(
        manager,
        field_kind="sphere",
        args=["NF1"],
        kwargs={"radius": "10mm"},
    )
    assert traces["traces"]["traces"] == ["dB(S(1,1))"]
    assert touchstone["touchstone_data"]["sweep"] == "Sweep1"
    assert monitors["monitor_data"][0]["name"] == "Monitor1"
    assert near_field["method"] == "insert_near_field_sphere"
    assert near_field["result"]["radius"] == "10mm"


def test_export_diagnostics_uses_allowlisted_methods() -> None:
    result = export_diagnostics(
        active_manager(),
        export_kind="convergence",
        setup="Setup1",
        variations="w=10mm",
        output_file="convergence.csv",
    )
    assert result["method"] == "export_convergence"
    assert result["result"]["output_file"] == "convergence.csv"


def test_solver_specific_operation_wrappers_dispatch_allowlisted_methods() -> None:
    manager = active_manager()
    hfss = hfss_operation(
        manager,
        method="create_scattering",
        kwargs={"plot": "S11", "ports": ["P1"]},
    )
    maxwell = maxwell_operation(
        manager,
        method="assign_winding",
        kwargs={"assignment": ["Coil1"], "name": "Winding1", "current": 2},
    )
    q3d = q3d_operation(
        manager,
        method="assign_net",
        args=[["Face1"]],
        kwargs={"net_name": "Net1"},
    )
    icepak = icepak_operation(
        manager,
        method="assign_source",
        args=["Block1", "Total Power", "3W"],
    )
    circuit = circuit_operation(
        manager,
        method="create_schematic_from_netlist",
        args=["design.net"],
    )
    assert hfss["result"]["ports"] == ["P1"]
    assert maxwell["result"]["name"] == "Winding1"
    assert q3d["result"]["net_name"] == "Net1"
    assert icepak["result"]["assignment_value"] == "3W"
    assert circuit["result"]["input_file"] == "design.net"


def test_matrix_and_icepak_summary_exports_dispatch_to_app() -> None:
    manager = active_manager()
    matrix = export_matrix_data(
        manager,
        export_kind="q3d",
        args=["matrix.csv"],
        kwargs={"setup": "Setup1"},
    )
    summary = export_icepak_summary(
        manager,
        output_dir="out",
        solution_name="Setup1",
        quantity="Temperature",
        filename="summary.csv",
    )
    assert matrix["method"] == "export_matrix_data"
    assert matrix["result"]["file_name"] == "matrix.csv"
    assert summary["method"] == "export_summary"
    assert summary["result"]["filename"] == "summary.csv"


def test_native_module_call_uses_get_module() -> None:
    manager = desktop_manager()
    new_project(manager, project_name="MCPNativeProject")
    result = native_module_call(manager, module_name="AnalysisSetup", method="GetSetups")
    assert result["module_name"] == "AnalysisSetup"
    assert result["result"] == ["Setup1"]


def test_native_property_wrappers_use_property_api() -> None:
    manager = desktop_manager()
    new_project(manager, project_name="MCPNativeProject")
    properties = native_get_properties(
        manager,
        target="oproject",
        tab="ProjectVariableTab",
        server="ProjectVariables",
    )
    value = native_get_property_value(
        manager,
        target="oproject",
        tab="ProjectVariableTab",
        server="ProjectVariables",
        property_name="$w",
    )
    changed = native_change_property(
        manager,
        target="oproject",
        change_payload=["NAME:AllTabs"],
    )
    assert properties["properties"] == ["ProjectVariableTab:ProjectVariables:Prop"]
    assert value["value"] == "ProjectVariableTab:ProjectVariables:$w:Value"
    assert changed["result"] == {"changed": ["NAME:AllTabs"]}
