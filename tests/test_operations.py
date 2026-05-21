from __future__ import annotations

import pytest

from ansysmcp.operations import (
    assign_boundary_or_excitation,
    assign_material,
    create_dataset,
    create_field_plot,
    create_optimization,
    design_summary,
    export_app_data,
    import_dataset,
    insert_design,
    invoke,
    list_api,
    list_projects,
    mesh_operation,
    native_module_call,
    new_project,
    set_active_design,
    set_active_project,
    set_variable,
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

    def create_box(self, position, dimensions, name=None, matname=None):
        self.created.append((position, dimensions, name, matname))
        return {"name": name, "material": matname}


class DummyOptimizations:
    def add(self, calculation=None, ranges=None, variables=None, optimization_type="Optimization"):
        return {
            "calculation": calculation,
            "ranges": ranges,
            "variables": variables,
            "optimization_type": optimization_type,
        }


class DummyPost:
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


class DummyMesh:
    def assign_length_mesh(self, assignment, maximum_length):
        return {"assignment": assignment, "maximum_length": maximum_length}


class DummyApp:
    def __init__(self) -> None:
        self.variable_manager = DummyVariableManager()
        self.modeler = DummyModeler()
        self.optimizations = DummyOptimizations()
        self.post = DummyPost()
        self.mesh = DummyMesh()
        self.boundaries = ["Boundary1"]
        self.setups = ["Setup1"]

    def echo(self, value: str) -> str:
        return value

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


def test_native_module_call_uses_get_module() -> None:
    manager = desktop_manager()
    new_project(manager, project_name="MCPNativeProject")
    result = native_module_call(manager, module_name="AnalysisSetup", method="GetSetups")
    assert result["module_name"] == "AnalysisSetup"
    assert result["result"] == ["Setup1"]
