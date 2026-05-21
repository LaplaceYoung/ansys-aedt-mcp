from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ansysmcp.serialization import to_jsonable
from ansysmcp.session import AedtError, AedtSessionManager, call_with_supported_kwargs

BLOCKED_ATTR_PREFIXES = ("_",)
EXPORT_METHODS: dict[str, str] = {
    "3d_model": "export_3d_model",
    "antenna_metadata": "export_antenna_metadata",
    "convergence": "export_convergence",
    "design_preview": "export_design_preview_to_jpg",
    "element_pattern": "export_element_pattern",
    "mesh_stats": "export_mesh_stats",
    "parametric_results": "export_parametric_results",
    "profile": "export_profile",
    "results": "export_results",
    "touchstone": "export_touchstone",
    "variables": "export_variables_to_csv",
}


def list_api(obj: Any, *, include_private: bool = False) -> dict[str, Any]:
    names = dir(obj)
    if not include_private:
        names = [name for name in names if not name.startswith("_")]
    methods: list[str] = []
    attributes: list[str] = []
    for name in names:
        try:
            value = getattr(obj, name)
        except Exception:
            attributes.append(name)
            continue
        if callable(value):
            methods.append(name)
        else:
            attributes.append(name)
    return {
        "type": f"{type(obj).__module__}.{type(obj).__name__}",
        "methods": sorted(methods),
        "attributes": sorted(attributes),
    }


def invoke(
    obj: Any,
    *,
    attr_path: str | list[str] | None = None,
    method: str | None = None,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
    allow_private: bool = False,
) -> Any:
    target = resolve_attr_path(obj, attr_path, allow_private=allow_private)
    if method:
        validate_attr_name(method, allow_private=allow_private)
        target = getattr(target, method)
    if callable(target):
        return target(*(args or []), **dict(kwargs or {}))
    if args or kwargs:
        raise AedtError("Resolved target is an attribute. Remove args/kwargs or provide a method.")
    return target


def resolve_attr_path(
    obj: Any,
    attr_path: str | list[str] | None,
    *,
    allow_private: bool = False,
) -> Any:
    target = obj
    for name in normalize_attr_path(attr_path):
        validate_attr_name(name, allow_private=allow_private)
        target = getattr(target, name)
    return target


def normalize_attr_path(attr_path: str | list[str] | None) -> list[str]:
    if attr_path is None or attr_path == "":
        return []
    if isinstance(attr_path, str):
        return [part for part in attr_path.split(".") if part]
    return list(attr_path)


def validate_attr_name(name: str, *, allow_private: bool = False) -> None:
    if allow_private:
        return
    if name.startswith(BLOCKED_ATTR_PREFIXES) or "__" in name:
        raise AedtError(f"Private or magic attribute access is blocked: {name}")


def set_variable(
    manager: AedtSessionManager,
    *,
    name: str,
    expression: str | int | float,
    description: str | None = None,
    sweep: bool | None = None,
    hidden: bool | None = None,
    read_only: bool | None = None,
) -> dict[str, Any]:
    app = manager.app
    vm = getattr(app, "variable_manager", None)
    if vm is not None and hasattr(vm, "set_variable"):
        result = call_with_supported_kwargs(
            vm.set_variable,
            {
                "name": name,
                "expression": expression,
                "description": description,
                "sweep": sweep,
                "hidden": hidden,
                "read_only": read_only,
            },
            positional_fallback=[name, expression],
        )
    else:
        app[name] = expression
        result = True
    return {"name": name, "expression": expression, "result": to_jsonable(result)}


def get_variables(manager: AedtSessionManager) -> dict[str, Any]:
    app = manager.app
    vm = getattr(app, "variable_manager", None)
    if vm is None:
        return {}
    output: dict[str, Any] = {}
    for attr in (
        "variable_names",
        "project_variable_names",
        "design_variable_names",
        "dependent_variable_names",
        "independent_variable_names",
        "independent_project_variable_names",
        "independent_design_variable_names",
    ):
        if hasattr(vm, attr):
            output[attr] = to_jsonable(getattr(vm, attr))
    for attr in ("variables", "project_variables", "design_variables"):
        if hasattr(vm, attr):
            raw = getattr(vm, attr)
            output[attr] = {
                str(name): variable_expression(vm, name, value) for name, value in dict(raw).items()
            }
    return output


def variable_expression(vm: Any, name: str, variable_obj: Any) -> Any:
    if hasattr(vm, "get_expression"):
        try:
            return vm.get_expression(name)
        except Exception:
            pass
    if hasattr(variable_obj, "expression"):
        try:
            return variable_obj.expression
        except Exception:
            pass
    return to_jsonable(variable_obj)


def create_setup(
    manager: AedtSessionManager,
    *,
    name: str | None = None,
    setup_type: str | None = None,
    properties: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "create_setup"):
        raise AedtError("Active app does not expose create_setup.")
    setup = call_with_supported_kwargs(
        app.create_setup,
        {"name": name, "setupname": name, "setup_type": setup_type},
        positional_fallback=[] if name is None else [name],
    )
    if properties:
        apply_setup_properties(setup, properties)
    if hasattr(setup, "update"):
        setup.update()
    return {"setup": to_jsonable(setup)}


def apply_setup_properties(setup: Any, properties: Mapping[str, Any]) -> None:
    props = getattr(setup, "props", None)
    if isinstance(props, dict):
        props.update(dict(properties))
        return
    for key, value in properties.items():
        try:
            setup[key] = value
        except Exception:
            setattr(setup, key, value)


def analyze(
    manager: AedtSessionManager,
    *,
    setup_name: str | None = None,
    analyze_all: bool = False,
) -> dict[str, Any]:
    app = manager.app
    if analyze_all and hasattr(app, "analyze"):
        return {"result": to_jsonable(app.analyze())}
    if setup_name and hasattr(app, "analyze_setup"):
        return {"result": to_jsonable(app.analyze_setup(setup_name))}
    if hasattr(app, "analyze"):
        return {"result": to_jsonable(app.analyze())}
    raise AedtError("Active app does not expose analyze or analyze_setup.")


def create_parametric_sweep(
    manager: AedtSessionManager,
    *,
    variable: str,
    start: str | int | float,
    stop: str | int | float,
    step: str | int | float,
    name: str | None = None,
    variation_type: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    parametrics = getattr(app, "parametrics", None)
    if parametrics is None or not hasattr(parametrics, "add"):
        raise AedtError("Active app does not expose parametrics.add.")
    result = call_with_supported_kwargs(
        parametrics.add,
        {
            "variable": variable,
            "start_point": start,
            "end_point": stop,
            "step": step,
            "name": name,
            "variation_type": variation_type,
        },
        positional_fallback=[variable, start, stop, step],
    )
    return {"parametric": to_jsonable(result)}


def create_geometry(
    manager: AedtSessionManager,
    *,
    primitive: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    modeler = manager.target("modeler")
    method_name = primitive if primitive.startswith("create_") else f"create_{primitive}"
    validate_attr_name(method_name)
    if not hasattr(modeler, method_name):
        raise AedtError(f"Modeler does not expose '{method_name}'.")
    result = getattr(modeler, method_name)(*(args or []), **dict(kwargs or {}))
    return {"object": to_jsonable(result)}


def run_app_method(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    validate_attr_name(method)
    if not hasattr(app, method):
        raise AedtError(f"Active app does not expose '{method}'.")
    result = getattr(app, method)(*(args or []), **dict(kwargs or {}))
    return {"result": to_jsonable(result)}


def list_projects(manager: AedtSessionManager) -> dict[str, Any]:
    desktop = manager.target("desktop")
    project_names = to_jsonable(getattr(desktop, "project_list", []))
    designs: dict[str, Any] = {}
    if hasattr(desktop, "design_list"):
        for project_name in project_names:
            try:
                designs[str(project_name)] = to_jsonable(desktop.design_list(project=project_name))
            except Exception as exc:
                designs[str(project_name)] = {"error": str(exc)}
    return {
        "active_project_name": to_jsonable(getattr(desktop, "active_project_name", None)),
        "active_design_name": to_jsonable(getattr(desktop, "active_design_name", None)),
        "projects": project_names,
        "designs": designs,
    }


def new_project(
    manager: AedtSessionManager,
    *,
    project_name: str | None = None,
) -> dict[str, Any]:
    odesktop = manager.target("odesktop")
    if not hasattr(odesktop, "NewProject"):
        raise AedtError("AEDT Desktop native object does not expose NewProject.")
    project = odesktop.NewProject()
    if project_name:
        project.Rename(project_name, True)
    created_name = project.GetName() if hasattr(project, "GetName") else project_name
    return {
        "project_name": to_jsonable(created_name),
        "project": to_jsonable(project),
        "projects": list_projects(manager),
    }


def insert_design(
    manager: AedtSessionManager,
    *,
    design_type: str,
    design_name: str,
    solution_type: str = "",
    project_name: str | None = None,
) -> dict[str, Any]:
    desktop = manager.target("desktop")
    project = None
    if project_name and hasattr(desktop, "active_project"):
        project = desktop.active_project(project_name)
    if project is None and hasattr(desktop, "active_project"):
        project = desktop.active_project()
    if project is None:
        project = manager.target("odesktop").NewProject()
    if not hasattr(project, "InsertDesign"):
        raise AedtError("AEDT project object does not expose InsertDesign.")
    result = project.InsertDesign(design_type, design_name, solution_type, "")
    return {
        "result": to_jsonable(result),
        "design_name": design_name,
        "designs": list_projects(manager),
    }


def assign_material(
    manager: AedtSessionManager,
    *,
    assignment: str | list[str],
    material: str,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "assign_material"):
        raise AedtError("Active app does not expose assign_material.")
    result = app.assign_material(assignment, material)
    return {"assignment": assignment, "material": material, "result": to_jsonable(result)}


def create_dataset(
    manager: AedtSessionManager,
    *,
    name: str,
    x: list[Any],
    y: list[Any],
    z: list[Any] | None = None,
    v: list[Any] | None = None,
    is_project_dataset: bool = True,
    x_unit: str = "",
    y_unit: str = "",
    z_unit: str = "",
    v_unit: str = "",
    sort: bool = True,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "create_dataset"):
        raise AedtError("Active app does not expose create_dataset.")
    result = app.create_dataset(
        name=name,
        x=x,
        y=y,
        z=z,
        v=v,
        is_project_dataset=is_project_dataset,
        x_unit=x_unit,
        y_unit=y_unit,
        z_unit=z_unit,
        v_unit=v_unit,
        sort=sort,
    )
    return {"dataset": to_jsonable(result)}


def import_dataset(
    manager: AedtSessionManager,
    *,
    input_file: str,
    dimensions: int = 1,
    name: str | None = None,
    is_project_dataset: bool = True,
    sort: bool = True,
    encoding: str = "utf-8-sig",
) -> dict[str, Any]:
    app = manager.app
    method_name = "import_dataset3d" if dimensions == 3 else "import_dataset1d"
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = call_with_supported_kwargs(
        getattr(app, method_name),
        {
            "input_file": input_file,
            "name": name,
            "is_project_dataset": is_project_dataset,
            "sort": sort,
            "encoding": encoding,
        },
        positional_fallback=[input_file],
    )
    return {"dataset": to_jsonable(result)}


def create_optimization(
    manager: AedtSessionManager,
    *,
    calculation: str | None = None,
    ranges: Mapping[str, Any] | None = None,
    variables: list[Any] | None = None,
    optimization_type: str = "Optimization",
    condition: str = "<=",
    goal_value: int | float = 1,
    goal_weight: int | float = 1,
    solution: str | None = None,
    name: str | None = None,
    context: str | None = None,
    report_type: str | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    optimizations = getattr(app, "optimizations", None)
    if optimizations is None or not hasattr(optimizations, "add"):
        raise AedtError("Active app does not expose optimizations.add.")
    result = call_with_supported_kwargs(
        optimizations.add,
        {
            "calculation": calculation,
            "ranges": ranges,
            "variables": variables,
            "optimization_type": optimization_type,
            "condition": condition,
            "goal_value": goal_value,
            "goal_weight": goal_weight,
            "solution": solution,
            "name": name,
            "context": context,
            "report_type": report_type,
            **dict(kwargs or {}),
        },
    )
    return {"optimization": to_jsonable(result)}


def create_field_plot(
    manager: AedtSessionManager,
    *,
    plot_kind: str,
    assignment: str | list[str],
    quantity: str,
    setup: str | None = None,
    intrinsics: str | Mapping[str, str] | None = None,
    plot_name: str | None = None,
    field_type: str = "DC R/L Fields",
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    post = manager.target("post")
    normalized = plot_kind.lower().replace("-", "_").replace(" ", "_")
    method_map = {
        "surface": "create_fieldplot_surface",
        "cutplane": "create_fieldplot_cutplane",
        "cut_plane": "create_fieldplot_cutplane",
        "volume": "create_fieldplot_volume",
    }
    method_name = method_map.get(normalized)
    if method_name is None:
        raise AedtError("plot_kind must be one of surface, cutplane, or volume.")
    if not hasattr(post, method_name):
        raise AedtError(f"Post object does not expose {method_name}.")
    result = call_with_supported_kwargs(
        getattr(post, method_name),
        {
            "assignment": assignment,
            "quantity": quantity,
            "setup": setup,
            "intrinsics": intrinsics,
            "plot_name": plot_name,
            "field_type": field_type,
            **dict(kwargs or {}),
        },
        positional_fallback=[assignment, quantity],
    )
    return {"field_plot": to_jsonable(result)}


def export_field_plot(
    manager: AedtSessionManager,
    *,
    plot_name: str,
    output_dir: str,
    file_name: str = "",
    file_format: str = "aedtplt",
) -> dict[str, Any]:
    post = manager.target("post")
    if not hasattr(post, "export_field_plot"):
        raise AedtError("Post object does not expose export_field_plot.")
    Path(output_dir).expanduser().mkdir(parents=True, exist_ok=True)
    result = post.export_field_plot(
        plot_name=plot_name,
        output_dir=output_dir,
        file_name=file_name,
        file_format=file_format,
    )
    return {"result": to_jsonable(result)}


def export_app_data(
    manager: AedtSessionManager,
    *,
    export_kind: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    normalized = export_kind.lower().replace("-", "_").replace(" ", "_")
    method_name = EXPORT_METHODS.get(normalized)
    if method_name is None:
        supported = ", ".join(sorted(EXPORT_METHODS))
        raise AedtError(f"Unsupported export_kind '{export_kind}'. Supported values: {supported}.")
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = getattr(app, method_name)(*(args or []), **dict(kwargs or {}))
    return {"export_kind": normalized, "result": to_jsonable(result)}


def create_report(
    manager: AedtSessionManager,
    *,
    expressions: str | list[str],
    report_category: str = "standard",
    setup_name: str | None = None,
    variations: Mapping[str, Any] | None = None,
    context: Any = None,
    report_name: str | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    post = manager.target("post")
    extra = dict(kwargs or {})
    if hasattr(post, "create_report"):
        result = call_with_supported_kwargs(
            post.create_report,
            {
                "expressions": expressions,
                "expression": expressions,
                "setup_sweep_name": setup_name,
                "setup_name": setup_name,
                "variations": variations,
                "context": context,
                "report_category": report_category,
                "plotname": report_name,
                "report_name": report_name,
                **extra,
            },
            positional_fallback=[expressions],
        )
        return {"report": to_jsonable(result)}

    reports_by_category = getattr(post, "reports_by_category", None)
    if reports_by_category is None:
        raise AedtError("Post object does not expose create_report or reports_by_category.")
    category_method = report_category.lower().replace(" ", "_").replace("-", "_")
    validate_attr_name(category_method)
    if not hasattr(reports_by_category, category_method):
        raise AedtError(f"reports_by_category does not expose '{category_method}'.")
    category_factory = getattr(reports_by_category, category_method)
    report = category_factory(expressions, setup_name, context, **extra)
    if report_name and hasattr(report, "plot_name"):
        report.plot_name = report_name
    if variations and hasattr(report, "variations"):
        report.variations = dict(variations)
    created = report.create() if hasattr(report, "create") else report
    return {"created": to_jsonable(created), "report": to_jsonable(report)}


def get_solution_data(
    manager: AedtSessionManager,
    *,
    expressions: str | list[str],
    setup_name: str | None = None,
    variations: Mapping[str, Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    post = manager.target("post")
    if not hasattr(post, "get_solution_data"):
        raise AedtError("Post object does not expose get_solution_data.")
    result = call_with_supported_kwargs(
        post.get_solution_data,
        {
            "expressions": expressions,
            "expression": expressions,
            "setup_sweep_name": setup_name,
            "setup_name": setup_name,
            "variations": variations,
            **dict(kwargs or {}),
        },
        positional_fallback=[expressions],
    )
    return {"solution_data": to_jsonable(result)}


def export_report(
    manager: AedtSessionManager,
    *,
    report_name: str,
    output_path: str,
    file_format: str = "csv",
) -> dict[str, Any]:
    post = manager.target("post")
    path = Path(output_path).expanduser()
    file_path = path if path.suffix else path / f"{report_name}.{file_format.lstrip('.')}"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    for method_name in ("export_report_to_file", "export_report"):
        if hasattr(post, method_name):
            result = getattr(post, method_name)(report_name, str(file_path))
            return {"path": str(file_path), "result": to_jsonable(result)}

    app = manager.app
    if hasattr(app, "odesign"):
        module = app.odesign.GetModule("ReportSetup")
        result = module.ExportToFile(report_name, str(file_path), False)
        return {"path": str(file_path), "result": to_jsonable(result)}
    raise AedtError("No report export method is available.")
