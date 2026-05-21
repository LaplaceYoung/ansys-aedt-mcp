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
ASSIGNMENT_METHOD_PREFIXES = ("assign_", "create_")
DELETE_METHODS = {
    "delete_design",
    "delete_project",
    "delete_setup",
    "delete_unused_variables",
    "delete_variable",
}
PORT_METHODS = {
    "circuit_port",
    "create_floquet_port",
    "create_spiral_lumped_port",
    "lumped_port",
    "wave_port",
}
SWEEP_METHODS = {
    "linear_count": "create_linear_count_sweep",
    "linear_step": "create_linear_step_sweep",
    "single_point": "create_single_point_sweep",
}
DIAGNOSTIC_EXPORT_METHODS = {
    "convergence": "export_convergence",
    "mesh_stats": "export_mesh_stats",
    "profile": "export_profile",
}
HFSS_OPERATION_METHODS = {
    "assign_current_source_to_sheet",
    "assign_febi",
    "assign_finite_conductivity",
    "assign_hybrid_region",
    "assign_impedance_to_sheet",
    "assign_layered_impedance",
    "assign_lumped_rlc_to_sheet",
    "assign_perfect_e",
    "assign_perfect_h",
    "assign_primary",
    "assign_radiation_boundary_to_faces",
    "assign_radiation_boundary_to_objects",
    "assign_secondary",
    "assign_symmetry",
    "assign_voltage_source_to_sheet",
    "auto_assign_lattice_pairs",
    "create_boundary",
    "create_current_source_from_objects",
    "create_impedance_between_objects",
    "create_lumped_rlc_between_objects",
    "create_perfecte_from_objects",
    "create_perfecth_from_objects",
    "create_scattering",
    "create_source_excitation",
    "create_voltage_source_from_objects",
    "edit_sources",
    "set_source_context",
}
MAXWELL_OPERATION_METHODS = {
    "add_winding_coils",
    "assign_coil",
    "assign_current",
    "assign_current_density",
    "assign_current_density_terminal",
    "assign_floating",
    "assign_flux_tangential",
    "assign_force",
    "assign_impedance",
    "assign_insulating",
    "assign_layout_force",
    "assign_master_slave",
    "assign_matrix",
    "assign_radiation",
    "assign_resistive_sheet",
    "assign_rotate_motion",
    "assign_sink",
    "assign_symmetry",
    "assign_tangential_h_field",
    "assign_torque",
    "assign_translate_motion",
    "assign_voltage",
    "assign_voltage_drop",
    "assign_winding",
    "assign_zero_tangential_h_field",
    "create_external_circuit",
    "order_coil_terminals",
    "set_core_losses",
    "set_source_context",
    "solve_inside",
}
Q3D_OPERATION_METHODS = {
    "assign_net",
    "assign_thin_conductor",
    "edit_sources",
    "insert_reduced_matrix",
    "net_sources",
    "set_source_context",
    "source",
    "sources",
}
ICEPAK_OPERATION_METHODS = {
    "assign_2way_coupling",
    "assign_adiabatic_plate",
    "assign_blower_type1",
    "assign_blower_type2",
    "assign_conducting_plate",
    "assign_conducting_plate_with_conductance",
    "assign_conducting_plate_with_impedance",
    "assign_conducting_plate_with_resistance",
    "assign_conducting_plate_with_thickness",
    "assign_device_resistance",
    "assign_em_losses",
    "assign_free_opening",
    "assign_grille",
    "assign_hollow_block",
    "assign_loss_curve_resistance",
    "assign_mass_flow_free_opening",
    "assign_openings",
    "assign_point_monitor",
    "assign_point_monitor_in_object",
    "assign_power_law_resistance",
    "assign_pressure_free_opening",
    "assign_recirculation_opening",
    "assign_resistance",
    "assign_solid_block",
    "assign_source",
    "assign_stationary_wall",
    "assign_stationary_wall_with_heat_flux",
    "assign_stationary_wall_with_htc",
    "assign_stationary_wall_with_temperature",
    "assign_surface_material",
    "assign_surface_monitor",
    "assign_symmetry_wall",
    "assign_velocity_free_opening",
    "create_fan",
    "create_network_object",
    "create_parametric_heatsink_on_face",
    "create_source_blocks_from_list",
    "create_two_resistor_network_block",
    "generate_fluent_mesh",
    "globalMeshSettings",
    "set_source_context",
}
CIRCUIT_OPERATION_METHODS = {
    "assign_current_sinusoidal_excitation_to_ports",
    "assign_power_sinusoidal_excitation_to_ports",
    "assign_voltage_frequency_dependent_excitation_to_ports",
    "assign_voltage_sinusoidal_excitation_to_ports",
    "create_ami_schematic_from_snp",
    "create_ibis_schematic_from_pins",
    "create_ibis_schematic_from_snp",
    "create_lna_schematic_from_snp",
    "create_schematic_from_asc_file",
    "create_schematic_from_mentor_netlist",
    "create_schematic_from_netlist",
    "create_source",
    "create_tdr_schematic_from_snp",
    "create_touchstone_report",
    "export_fullwave_spice",
}
MATRIX_EXPORT_METHODS = {
    "maxwell": "export_matrix",
    "maxwell_matrix": "export_matrix",
    "q3d": "export_matrix_data",
    "q3d_matrix": "export_matrix_data",
    "equivalent_circuit": "export_equivalent_circuit",
    "q3d_equivalent_circuit": "export_equivalent_circuit",
}
PROJECT_DESIGN_OPERATION_METHODS = {
    "archive_project",
    "change_design_settings",
    "change_validation_settings",
    "check_if_project_is_loaded",
    "copy_design_from",
    "copy_project",
    "duplicate_design",
    "flatten_3d_components",
    "list_of_variations",
    "read_design_data",
    "rename_design",
    "validate_full_design",
    "validate_simple",
}
NEAR_FIELD_METHODS = {
    "box": "insert_near_field_box",
    "line": "insert_near_field_line",
    "points": "insert_near_field_points",
    "rectangle": "insert_near_field_rectangle",
    "sphere": "insert_near_field_sphere",
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


def batch_call(
    manager: AedtSessionManager,
    *,
    operations: list[Mapping[str, Any]],
    continue_on_error: bool = False,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for index, operation in enumerate(operations):
        try:
            target_name = str(operation.get("target", "app"))
            module_name = operation.get("module_name")
            target = manager.target(target_name, module_name=module_name)
            result = invoke(
                target,
                attr_path=operation.get("attr_path"),
                method=operation.get("method"),
                args=operation.get("args"),
                kwargs=operation.get("kwargs"),
                allow_private=bool(operation.get("allow_private", False)),
            )
            results.append(
                {
                    "index": index,
                    "ok": True,
                    "target": target_name,
                    "method": operation.get("method"),
                    "result": to_jsonable(result),
                }
            )
        except Exception as exc:
            results.append(
                {
                    "index": index,
                    "ok": False,
                    "target": operation.get("target", "app"),
                    "method": operation.get("method"),
                    "error": str(exc),
                }
            )
            if not continue_on_error:
                break
    return {
        "ok": all(item["ok"] for item in results),
        "completed": len(results),
        "requested": len(operations),
        "results": results,
    }


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


def setup_summary(manager: AedtSessionManager) -> dict[str, Any]:
    app = manager.app
    summary: dict[str, Any] = {}
    for attr in ("setup_names", "setup_sweeps_names", "active_setup", "nominal_sweep"):
        if hasattr(app, attr):
            try:
                summary[attr] = to_jsonable(getattr(app, attr))
            except Exception as exc:
                summary[attr] = {"error": str(exc)}
    if hasattr(app, "get_setups"):
        try:
            setups = app.get_setups()
            summary["get_setups"] = to_jsonable(setups)
            sweeps: dict[str, Any] = {}
            if hasattr(app, "get_sweeps"):
                for setup_name in setups:
                    try:
                        sweeps[str(setup_name)] = to_jsonable(app.get_sweeps(setup_name))
                    except Exception as exc:
                        sweeps[str(setup_name)] = {"error": str(exc)}
            summary["sweeps"] = sweeps
        except Exception as exc:
            summary["get_setups"] = {"error": str(exc)}
    return summary


def get_setup_properties(
    manager: AedtSessionManager,
    *,
    name: str,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_setup"):
        raise AedtError("Active app does not expose get_setup.")
    setup = app.get_setup(name)
    return {
        "name": name,
        "setup": to_jsonable(setup),
        "properties": to_jsonable(getattr(setup, "props", {})),
    }


def update_setup(
    manager: AedtSessionManager,
    *,
    name: str,
    properties: Mapping[str, Any],
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_setup"):
        raise AedtError("Active app does not expose get_setup.")
    setup = app.get_setup(name)
    apply_setup_properties(setup, properties)
    result = setup.update() if hasattr(setup, "update") else True
    return {
        "name": name,
        "result": to_jsonable(result),
        "properties": to_jsonable(getattr(setup, "props", {})),
    }


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


def analyze_setup(
    manager: AedtSessionManager,
    *,
    name: str | None = None,
    cores: int | None = None,
    tasks: int | None = None,
    gpus: int | None = None,
    acf_file: str | None = None,
    use_auto_settings: bool = True,
    num_variations_to_distribute: int | None = None,
    allowed_distribution_types: list[Any] | None = None,
    revert_to_initial_mesh: bool = False,
    blocking: bool = True,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "analyze_setup"):
        raise AedtError("Active app does not expose analyze_setup.")
    result = call_with_supported_kwargs(
        app.analyze_setup,
        {
            "name": name,
            "cores": cores,
            "tasks": tasks,
            "gpus": gpus,
            "acf_file": acf_file,
            "use_auto_settings": use_auto_settings,
            "num_variations_to_distribute": num_variations_to_distribute,
            "allowed_distribution_types": allowed_distribution_types,
            "revert_to_initial_mesh": revert_to_initial_mesh,
            "blocking": blocking,
        },
    )
    return {"setup": name, "result": to_jsonable(result)}


def solve_in_batch(
    manager: AedtSessionManager,
    *,
    file_name: str | None = None,
    machine: str = "localhost",
    run_in_thread: bool = False,
    cores: int = 4,
    tasks: int = 1,
    setup: str | None = None,
    revert_to_initial_mesh: bool = False,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "solve_in_batch"):
        raise AedtError("Active app does not expose solve_in_batch.")
    result = call_with_supported_kwargs(
        app.solve_in_batch,
        {
            "file_name": file_name,
            "machine": machine,
            "run_in_thread": run_in_thread,
            "cores": cores,
            "tasks": tasks,
            "setup": setup,
            "revert_to_initial_mesh": revert_to_initial_mesh,
        },
    )
    return {"setup": setup, "result": to_jsonable(result)}


def apply_solved_variation(
    manager: AedtSessionManager,
    *,
    variation: Mapping[str, Any],
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "apply_solved_variation"):
        raise AedtError("Active app does not expose apply_solved_variation.")
    result = app.apply_solved_variation(dict(variation))
    return {"variation": to_jsonable(variation), "result": to_jsonable(result)}


def get_nominal_variation(
    manager: AedtSessionManager,
    *,
    with_values: bool = False,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_nominal_variation"):
        raise AedtError("Active app does not expose get_nominal_variation.")
    result = call_with_supported_kwargs(
        app.get_nominal_variation,
        {"with_values": with_values},
    )
    return {"variation": to_jsonable(result)}


def get_evaluated_value(
    manager: AedtSessionManager,
    *,
    name: str,
    units: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_evaluated_value"):
        raise AedtError("Active app does not expose get_evaluated_value.")
    result = call_with_supported_kwargs(
        app.get_evaluated_value,
        {"name": name, "units": units},
        positional_fallback=[name],
    )
    return {"name": name, "units": units, "value": to_jsonable(result)}


def get_output_variable(
    manager: AedtSessionManager,
    *,
    variable: str,
    solution: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_output_variable"):
        raise AedtError("Active app does not expose get_output_variable.")
    result = call_with_supported_kwargs(
        app.get_output_variable,
        {"variable": variable, "solution": solution},
        positional_fallback=[variable],
    )
    return {"variable": variable, "value": to_jsonable(result)}


def get_profile(
    manager: AedtSessionManager,
    *,
    name: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_profile"):
        raise AedtError("Active app does not expose get_profile.")
    result = call_with_supported_kwargs(app.get_profile, {"name": name})
    return {"name": name, "profile": to_jsonable(result)}


def validate_design(
    manager: AedtSessionManager,
    *,
    validation_kind: str = "simple",
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    normalized = validation_kind.lower().replace("-", "_").replace(" ", "_")
    method_name = "validate_full_design" if normalized == "full" else "validate_simple"
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = getattr(app, method_name)(*(args or []), **dict(kwargs or {}))
    return {"validation_kind": normalized, "method": method_name, "result": to_jsonable(result)}


def cleanup_solution(
    manager: AedtSessionManager,
    *,
    variations: str | list[Any] = "All",
    entire_solution: bool = True,
    field: bool = True,
    mesh: bool = True,
    linked_data: bool = True,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "cleanup_solution"):
        raise AedtError("Active app does not expose cleanup_solution.")
    result = call_with_supported_kwargs(
        app.cleanup_solution,
        {
            "variations": variations,
            "entire_solution": entire_solution,
            "field": field,
            "mesh": mesh,
            "linked_data": linked_data,
        },
    )
    return {"result": to_jsonable(result)}


def change_design_settings(
    manager: AedtSessionManager,
    *,
    settings: Mapping[str, Any],
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "change_design_settings"):
        raise AedtError("Active app does not expose change_design_settings.")
    result = app.change_design_settings(dict(settings))
    return {"settings": to_jsonable(settings), "result": to_jsonable(result)}


def change_validation_settings(
    manager: AedtSessionManager,
    *,
    entity_check_level: str = "Strict",
    ignore_unclassified: bool = False,
    skip_intersections: bool = False,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "change_validation_settings"):
        raise AedtError("Active app does not expose change_validation_settings.")
    result = call_with_supported_kwargs(
        app.change_validation_settings,
        {
            "entity_check_level": entity_check_level,
            "ignore_unclassified": ignore_unclassified,
            "skip_intersections": skip_intersections,
        },
    )
    return {"result": to_jsonable(result)}


def list_variations(
    manager: AedtSessionManager,
    *,
    setup: str | None = None,
    sweep: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "list_of_variations"):
        raise AedtError("Active app does not expose list_of_variations.")
    result = call_with_supported_kwargs(app.list_of_variations, {"setup": setup, "sweep": sweep})
    return {"variations": to_jsonable(result)}


def read_design_data(manager: AedtSessionManager) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "read_design_data"):
        raise AedtError("Active app does not expose read_design_data.")
    return {"design_data": to_jsonable(app.read_design_data())}


def project_design_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    if method not in PROJECT_DESIGN_OPERATION_METHODS:
        supported = ", ".join(sorted(PROJECT_DESIGN_OPERATION_METHODS))
        raise AedtError(f"Unsupported project/design operation '{method}'. Supported: {supported}.")
    app = manager.app
    if not hasattr(app, method):
        raise AedtError(f"Active app does not expose {method}.")
    result = getattr(app, method)(*(args or []), **dict(kwargs or {}))
    return {"method": method, "result": to_jsonable(result)}


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


def set_active_project(
    manager: AedtSessionManager,
    *,
    project_name: str,
) -> dict[str, Any]:
    desktop = manager.target("desktop")
    if hasattr(desktop, "active_project"):
        project = desktop.active_project(project_name)
        return {"project": to_jsonable(project), "projects": list_projects(manager)}
    raise AedtError("Desktop object does not expose active_project.")


def set_active_design(
    manager: AedtSessionManager,
    *,
    design_name: str,
    design_type: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    if hasattr(app, "set_active_design"):
        result = app.set_active_design(design_name)
        return {"result": to_jsonable(result), "session": manager.info()}
    desktop = manager.target("desktop")
    if hasattr(desktop, "active_design"):
        design = desktop.active_design(name=design_name, design_type=design_type)
        return {"design": to_jsonable(design), "projects": list_projects(manager)}
    raise AedtError("Active session does not expose a design activation method.")


def design_summary(manager: AedtSessionManager) -> dict[str, Any]:
    summary: dict[str, Any] = {"session": manager.info()}
    try:
        summary["projects"] = list_projects(manager)
    except Exception as exc:
        summary["projects"] = {"error": str(exc)}

    app = manager.app
    for attr in ("setups", "boundaries", "excitations", "design_datasets", "project_datasets"):
        if hasattr(app, attr):
            try:
                summary[attr] = to_jsonable(getattr(app, attr))
            except Exception as exc:
                summary[attr] = {"error": str(exc)}

    modeler = getattr(app, "modeler", None)
    if modeler is not None:
        for attr in ("object_names", "solid_names", "sheet_names", "line_names"):
            if hasattr(modeler, attr):
                try:
                    summary[f"modeler_{attr}"] = to_jsonable(getattr(modeler, attr))
                except Exception as exc:
                    summary[f"modeler_{attr}"] = {"error": str(exc)}
    return summary


def assign_boundary_or_excitation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    if not method.startswith(ASSIGNMENT_METHOD_PREFIXES):
        raise AedtError("Boundary/excitation methods must start with assign_ or create_.")
    app = manager.app
    if not hasattr(app, method):
        raise AedtError(f"Active app does not expose {method}.")
    result = getattr(app, method)(*(args or []), **dict(kwargs or {}))
    return {"method": method, "result": to_jsonable(result)}


def solver_operation(
    manager: AedtSessionManager,
    *,
    solver: str,
    method: str,
    allowed_methods: set[str],
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    if method not in allowed_methods:
        supported = ", ".join(sorted(allowed_methods))
        raise AedtError(
            f"Unsupported {solver} operation '{method}'. Supported methods: {supported}."
        )
    app = manager.app
    if not hasattr(app, method):
        raise AedtError(f"Active app does not expose {method}.")
    result = getattr(app, method)(*(args or []), **dict(kwargs or {}))
    return {"solver": solver, "method": method, "result": to_jsonable(result)}


def hfss_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return solver_operation(
        manager,
        solver="hfss",
        method=method,
        allowed_methods=HFSS_OPERATION_METHODS,
        args=args,
        kwargs=kwargs,
    )


def maxwell_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return solver_operation(
        manager,
        solver="maxwell",
        method=method,
        allowed_methods=MAXWELL_OPERATION_METHODS,
        args=args,
        kwargs=kwargs,
    )


def q3d_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return solver_operation(
        manager,
        solver="q3d",
        method=method,
        allowed_methods=Q3D_OPERATION_METHODS,
        args=args,
        kwargs=kwargs,
    )


def icepak_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return solver_operation(
        manager,
        solver="icepak",
        method=method,
        allowed_methods=ICEPAK_OPERATION_METHODS,
        args=args,
        kwargs=kwargs,
    )


def circuit_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return solver_operation(
        manager,
        solver="circuit",
        method=method,
        allowed_methods=CIRCUIT_OPERATION_METHODS,
        args=args,
        kwargs=kwargs,
    )


def create_port(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    if method not in PORT_METHODS:
        supported = ", ".join(sorted(PORT_METHODS))
        raise AedtError(f"Unsupported port method '{method}'. Supported methods: {supported}.")
    app = manager.app
    if not hasattr(app, method):
        raise AedtError(f"Active app does not expose {method}.")
    result = getattr(app, method)(*(args or []), **dict(kwargs or {}))
    return {"method": method, "result": to_jsonable(result)}


def source_port_summary(manager: AedtSessionManager) -> dict[str, Any]:
    app = manager.app
    summary: dict[str, Any] = {}
    for attr in ("ports", "sources", "excitations"):
        if hasattr(app, attr):
            try:
                summary[attr] = to_jsonable(getattr(app, attr))
            except Exception as exc:
                summary[attr] = {"error": str(exc)}
    for method_name in ("get_all_sources", "get_all_source_modes", "get_fresnel_floquet_ports"):
        if hasattr(app, method_name):
            try:
                summary[method_name] = to_jsonable(getattr(app, method_name)())
            except Exception as exc:
                summary[method_name] = {"error": str(exc)}
    return summary


def material_object_summary(
    manager: AedtSessionManager,
    *,
    assignment: list[Any] | None = None,
    prop_names: str | list[str] | None = None,
) -> dict[str, Any]:
    app = manager.app
    summary: dict[str, Any] = {}
    for method_name in ("get_all_conductors_names", "get_all_dielectrics_names"):
        if hasattr(app, method_name):
            try:
                summary[method_name] = to_jsonable(getattr(app, method_name)())
            except Exception as exc:
                summary[method_name] = {"error": str(exc)}
    if hasattr(app, "get_object_material_properties"):
        result = call_with_supported_kwargs(
            app.get_object_material_properties,
            {"assignment": assignment, "prop_names": prop_names},
        )
        summary["object_material_properties"] = to_jsonable(result)
    return summary


def create_frequency_sweep(
    manager: AedtSessionManager,
    *,
    sweep_kind: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    normalized = sweep_kind.lower().replace("-", "_").replace(" ", "_")
    method_name = SWEEP_METHODS.get(normalized, normalized)
    validate_attr_name(method_name)
    if not method_name.startswith("create_") or "sweep" not in method_name:
        raise AedtError("Sweep method must be a public create_*sweep method.")
    app = manager.app
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = getattr(app, method_name)(*(args or []), **dict(kwargs or {}))
    return {"method": method_name, "result": to_jsonable(result)}


def export_diagnostics(
    manager: AedtSessionManager,
    *,
    export_kind: str,
    setup: str,
    variations: str = "",
    output_file: str | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    normalized = export_kind.lower().replace("-", "_").replace(" ", "_")
    method_name = DIAGNOSTIC_EXPORT_METHODS.get(normalized)
    if method_name is None:
        supported = ", ".join(sorted(DIAGNOSTIC_EXPORT_METHODS))
        raise AedtError(f"Unsupported diagnostic export '{export_kind}'. Supported: {supported}.")
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    export_kwargs = {
        "setup": setup,
        "variations": variations,
        "output_file": output_file,
        **dict(kwargs or {}),
    }
    result = call_with_supported_kwargs(
        getattr(app, method_name),
        export_kwargs,
        positional_fallback=[setup],
    )
    return {"export_kind": normalized, "method": method_name, "result": to_jsonable(result)}


def export_matrix_data(
    manager: AedtSessionManager,
    *,
    export_kind: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    normalized = export_kind.lower().replace("-", "_").replace(" ", "_")
    method_name = MATRIX_EXPORT_METHODS.get(normalized)
    if method_name is None:
        supported = ", ".join(sorted(MATRIX_EXPORT_METHODS))
        raise AedtError(f"Unsupported matrix export '{export_kind}'. Supported: {supported}.")
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = getattr(app, method_name)(*(args or []), **dict(kwargs or {}))
    return {"export_kind": normalized, "method": method_name, "result": to_jsonable(result)}


def export_icepak_summary(
    manager: AedtSessionManager,
    *,
    output_dir: str | None = None,
    solution_name: str | None = None,
    summary_type: str = "Object",
    geometry_type: str = "Volume",
    quantity: str = "Temperature",
    variation: str = "",
    variation_list: list[Any] | None = None,
    filename: str = "IPKsummaryReport",
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "export_summary"):
        raise AedtError("Active app does not expose export_summary.")
    result = call_with_supported_kwargs(
        app.export_summary,
        {
            "output_dir": output_dir,
            "solution_name": solution_name,
            "type": summary_type,
            "geometry_type": geometry_type,
            "quantity": quantity,
            "variation": variation,
            "variation_list": variation_list,
            "filename": filename,
        },
    )
    return {"method": "export_summary", "result": to_jsonable(result)}


def create_open_region(
    manager: AedtSessionManager,
    *,
    frequency: str | int | float | None = "1GHz",
    boundary: str = "Radiation",
    apply_infinite_ground: bool = False,
    gp_axis: str = "-z",
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "create_open_region"):
        raise AedtError("Active app does not expose create_open_region.")
    result = app.create_open_region(
        frequency=frequency,
        boundary=boundary,
        apply_infinite_ground=apply_infinite_ground,
        gp_axis=gp_axis,
    )
    return {"result": to_jsonable(result)}


def create_output_variable(
    manager: AedtSessionManager,
    *,
    variable: str,
    expression: str,
    solution: str | None = None,
    context: str | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "create_output_variable"):
        raise AedtError("Active app does not expose create_output_variable.")
    result = call_with_supported_kwargs(
        app.create_output_variable,
        {
            "variable": variable,
            "expression": expression,
            "solution": solution,
            "context": context,
        },
        positional_fallback=[variable, expression],
    )
    return {"variable": variable, "result": to_jsonable(result)}


def get_traces_for_plot(
    manager: AedtSessionManager,
    *,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_traces_for_plot"):
        raise AedtError("Active app does not expose get_traces_for_plot.")
    result = app.get_traces_for_plot(**dict(kwargs or {}))
    return {"traces": to_jsonable(result)}


def get_touchstone_data(
    manager: AedtSessionManager,
    *,
    setup: str | None = None,
    sweep: str | None = None,
    variations: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_touchstone_data"):
        raise AedtError("Active app does not expose get_touchstone_data.")
    result = app.get_touchstone_data(setup=setup, sweep=sweep, variations=variations)
    return {"touchstone_data": to_jsonable(result)}


def get_monitor_data(manager: AedtSessionManager) -> dict[str, Any]:
    app = manager.app
    if not hasattr(app, "get_monitor_data"):
        raise AedtError("Active app does not expose get_monitor_data.")
    return {"monitor_data": to_jsonable(app.get_monitor_data())}


def insert_near_field(
    manager: AedtSessionManager,
    *,
    field_kind: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    normalized = field_kind.lower().replace("-", "_").replace(" ", "_")
    method_name = NEAR_FIELD_METHODS.get(normalized)
    if method_name is None:
        supported = ", ".join(sorted(NEAR_FIELD_METHODS))
        raise AedtError(f"Unsupported near-field kind '{field_kind}'. Supported: {supported}.")
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = getattr(app, method_name)(*(args or []), **dict(kwargs or {}))
    return {"field_kind": normalized, "method": method_name, "result": to_jsonable(result)}


def import_cad(
    manager: AedtSessionManager,
    *,
    input_file: str,
    import_kind: str | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    app = manager.app
    suffix = Path(input_file).suffix.lower().lstrip(".")
    inferred = {
        "dxf": "import_dxf",
        "gds": "import_gds_3d",
        "gdsii": "import_gds_3d",
        "idf": "import_idf",
    }.get(suffix, "import_3d_cad")
    method_name = import_kind or inferred
    validate_attr_name(method_name)
    if not method_name.startswith("import_"):
        raise AedtError("CAD import method must start with import_.")
    if not hasattr(app, method_name):
        raise AedtError(f"Active app does not expose {method_name}.")
    result = getattr(app, method_name)(input_file, **dict(kwargs or {}))
    return {"method": method_name, "input_file": input_file, "result": to_jsonable(result)}


def delete_item(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    if method not in DELETE_METHODS:
        supported = ", ".join(sorted(DELETE_METHODS))
        raise AedtError(f"Unsupported delete method '{method}'. Supported methods: {supported}.")
    app = manager.app
    if not hasattr(app, method):
        raise AedtError(f"Active app does not expose {method}.")
    result = getattr(app, method)(*(args or []), **dict(kwargs or {}))
    return {"method": method, "result": to_jsonable(result)}


def mesh_operation(
    manager: AedtSessionManager,
    *,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    mesh = manager.target("mesh")
    if not hasattr(mesh, method):
        raise AedtError(f"Mesh object does not expose {method}.")
    result = getattr(mesh, method)(*(args or []), **dict(kwargs or {}))
    return {"method": method, "result": to_jsonable(result)}


def native_module_call(
    manager: AedtSessionManager,
    *,
    module_name: str,
    method: str,
    args: list[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_attr_name(method)
    module = manager.target("omodule", module_name=module_name)
    if not hasattr(module, method):
        raise AedtError(f"AEDT module {module_name} does not expose {method}.")
    result = getattr(module, method)(*(args or []), **dict(kwargs or {}))
    return {
        "module_name": module_name,
        "method": method,
        "result": to_jsonable(result),
    }


def native_get_properties(
    manager: AedtSessionManager,
    *,
    target: str,
    tab: str,
    server: str,
    module_name: str | None = None,
) -> dict[str, Any]:
    obj = manager.target(target, module_name=module_name)
    if not hasattr(obj, "GetProperties"):
        raise AedtError(f"Target {target} does not expose GetProperties.")
    result = obj.GetProperties(tab, server)
    return {"target": target, "tab": tab, "server": server, "properties": to_jsonable(result)}


def native_get_property_value(
    manager: AedtSessionManager,
    *,
    target: str,
    tab: str,
    server: str,
    property_name: str,
    module_name: str | None = None,
) -> dict[str, Any]:
    obj = manager.target(target, module_name=module_name)
    if not hasattr(obj, "GetPropertyValue"):
        raise AedtError(f"Target {target} does not expose GetPropertyValue.")
    result = obj.GetPropertyValue(tab, server, property_name)
    return {
        "target": target,
        "tab": tab,
        "server": server,
        "property_name": property_name,
        "value": to_jsonable(result),
    }


def native_change_property(
    manager: AedtSessionManager,
    *,
    target: str,
    change_payload: list[Any],
    module_name: str | None = None,
) -> dict[str, Any]:
    obj = manager.target(target, module_name=module_name)
    if not hasattr(obj, "ChangeProperty"):
        raise AedtError(f"Target {target} does not expose ChangeProperty.")
    result = obj.ChangeProperty(change_payload)
    return {"target": target, "result": to_jsonable(result)}


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
