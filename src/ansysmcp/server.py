from __future__ import annotations

import argparse
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP

from ansysmcp.operations import (
    analyze,
    assign_boundary_or_excitation,
    assign_material,
    create_dataset,
    create_field_plot,
    create_geometry,
    create_optimization,
    create_parametric_sweep,
    create_report,
    create_setup,
    design_summary,
    export_app_data,
    export_field_plot,
    export_report,
    get_solution_data,
    get_variables,
    import_dataset,
    insert_design,
    invoke,
    list_api,
    list_projects,
    mesh_operation,
    native_module_call,
    new_project,
    run_app_method,
    set_active_design,
    set_active_project,
    set_variable,
)
from ansysmcp.serialization import to_jsonable
from ansysmcp.session import AedtSessionManager, environment_report

mcp = FastMCP("Ansys Electronics Desktop MCP")
manager = AedtSessionManager()


@mcp.tool()
def aedt_environment() -> dict[str, Any]:
    """Inspect Python and PyAEDT availability without launching AEDT."""
    return environment_report()


@mcp.tool()
def aedt_start_session(
    app_name: str = "hfss",
    version: str | None = None,
    project: str | None = None,
    design: str | None = None,
    solution_type: str | None = None,
    non_graphical: bool = False,
    new_desktop: bool = True,
    close_on_exit: bool = False,
    student_version: bool = False,
    machine: str | None = None,
    port: int | None = None,
    aedt_process_id: int | None = None,
    extra_kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Launch or connect to an AEDT application through PyAEDT."""
    return manager.start(
        app_name,
        version=version,
        project=project,
        design=design,
        solution_type=solution_type,
        non_graphical=non_graphical,
        new_desktop=new_desktop,
        close_on_exit=close_on_exit,
        student_version=student_version,
        machine=machine,
        port=port,
        aedt_process_id=aedt_process_id,
        extra_kwargs=extra_kwargs,
    )


@mcp.tool()
def aedt_release_session(
    close_projects: bool = False,
    close_desktop: bool = False,
) -> dict[str, Any]:
    """Release the active AEDT session."""
    return manager.release(close_projects=close_projects, close_desktop=close_desktop)


@mcp.tool()
def aedt_session_info() -> dict[str, Any]:
    """Return active AEDT app, project, design, and version context."""
    return manager.info()


@mcp.tool()
def aedt_open_project(project_path: str, design_name: str | None = None) -> dict[str, Any]:
    """Open an AEDT project file in the active desktop session."""
    return manager.open_project(project_path, design_name)


@mcp.tool()
def aedt_save_project(
    project_name: str | None = None,
    project_path: str | None = None,
    overwrite: bool = True,
) -> dict[str, Any]:
    """Save the active AEDT project."""
    return manager.save_project(
        project_name=project_name,
        project_path=project_path,
        overwrite=overwrite,
    )


@mcp.tool()
def aedt_list_projects() -> dict[str, Any]:
    """List AEDT projects and designs through the Desktop context."""
    with manager.locked():
        return list_projects(manager)


@mcp.tool()
def aedt_new_project(project_name: str | None = None) -> dict[str, Any]:
    """Create a new AEDT project through the native Desktop API."""
    with manager.locked():
        return new_project(manager, project_name=project_name)


@mcp.tool()
def aedt_insert_design(
    design_type: str,
    design_name: str,
    solution_type: str = "",
    project_name: str | None = None,
) -> dict[str, Any]:
    """Insert a design into an AEDT project through the native Project API."""
    with manager.locked():
        return insert_design(
            manager,
            design_type=design_type,
            design_name=design_name,
            solution_type=solution_type,
            project_name=project_name,
        )


@mcp.tool()
def aedt_set_active_project(project_name: str) -> dict[str, Any]:
    """Set the active AEDT project by name."""
    with manager.locked():
        return set_active_project(manager, project_name=project_name)


@mcp.tool()
def aedt_set_active_design(
    design_name: str,
    design_type: str | None = None,
) -> dict[str, Any]:
    """Set the active AEDT design by name."""
    with manager.locked():
        return set_active_design(manager, design_name=design_name, design_type=design_type)


@mcp.tool()
def aedt_design_summary() -> dict[str, Any]:
    """Return a compact summary of session, projects, setups, boundaries, and modeler objects."""
    with manager.locked():
        return design_summary(manager)


@mcp.tool()
def aedt_set_variable(
    name: str,
    expression: str,
    description: str | None = None,
    sweep: bool | None = None,
    hidden: bool | None = None,
    read_only: bool | None = None,
) -> dict[str, Any]:
    """Set a design variable or project variable. Prefix name with '$' for project variables."""
    with manager.locked():
        return set_variable(
            manager,
            name=name,
            expression=expression,
            description=description,
            sweep=sweep,
            hidden=hidden,
            read_only=read_only,
        )


@mcp.tool()
def aedt_get_variables() -> dict[str, Any]:
    """List project and design variables from PyAEDT VariableManager."""
    with manager.locked():
        return get_variables(manager)


@mcp.tool()
def aedt_create_dataset(
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
    """Create a 1D or 3D AEDT dataset."""
    with manager.locked():
        return create_dataset(
            manager,
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


@mcp.tool()
def aedt_import_dataset(
    input_file: str,
    dimensions: int = 1,
    name: str | None = None,
    is_project_dataset: bool = True,
    sort: bool = True,
    encoding: str = "utf-8-sig",
) -> dict[str, Any]:
    """Import a 1D or 3D dataset file into AEDT."""
    with manager.locked():
        return import_dataset(
            manager,
            input_file=input_file,
            dimensions=dimensions,
            name=name,
            is_project_dataset=is_project_dataset,
            sort=sort,
            encoding=encoding,
        )


@mcp.tool()
def aedt_create_geometry(
    primitive: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create geometry through app.modeler, for example primitive='box' maps to create_box."""
    with manager.locked():
        return create_geometry(manager, primitive=primitive, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_assign_material(assignment: str | list[str], material: str) -> dict[str, Any]:
    """Assign an AEDT material to one object or many objects."""
    with manager.locked():
        return assign_material(manager, assignment=assignment, material=material)


@mcp.tool()
def aedt_assign_boundary_or_excitation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call a public assign_/create_ boundary or excitation method on the active PyAEDT app."""
    with manager.locked():
        return assign_boundary_or_excitation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_mesh_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call a public mesh operation on app.mesh."""
    with manager.locked():
        return mesh_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_create_setup(
    name: str | None = None,
    setup_type: str | None = None,
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an AEDT solution setup and apply setup properties."""
    with manager.locked():
        return create_setup(manager, name=name, setup_type=setup_type, properties=properties)


@mcp.tool()
def aedt_analyze(setup_name: str | None = None, analyze_all: bool = False) -> dict[str, Any]:
    """Run analysis for a named setup or the active design."""
    with manager.locked():
        return analyze(manager, setup_name=setup_name, analyze_all=analyze_all)


@mcp.tool()
def aedt_create_parametric_sweep(
    variable: str,
    start: str,
    stop: str,
    step: str,
    name: str | None = None,
    variation_type: str | None = None,
) -> dict[str, Any]:
    """Create an Optimetrics parametric sweep for a variable."""
    with manager.locked():
        return create_parametric_sweep(
            manager,
            variable=variable,
            start=start,
            stop=stop,
            step=step,
            name=name,
            variation_type=variation_type,
        )


@mcp.tool()
def aedt_create_optimization(
    calculation: str | None = None,
    ranges: dict[str, Any] | None = None,
    variables: list[Any] | None = None,
    optimization_type: str = "Optimization",
    condition: str = "<=",
    goal_value: float = 1,
    goal_weight: float = 1,
    solution: str | None = None,
    name: str | None = None,
    context: str | None = None,
    report_type: str | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an Optimetrics optimization, sensitivity, statistical, DOE, or DX setup."""
    with manager.locked():
        return create_optimization(
            manager,
            calculation=calculation,
            ranges=ranges,
            variables=variables,
            optimization_type=optimization_type,
            condition=condition,
            goal_value=goal_value,
            goal_weight=goal_weight,
            solution=solution,
            name=name,
            context=context,
            report_type=report_type,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_create_report(
    expressions: str | list[str],
    report_category: str = "standard",
    setup_name: str | None = None,
    variations: dict[str, Any] | None = None,
    context: Any = None,
    report_name: str | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an AEDT report through PyAEDT post-processing."""
    with manager.locked():
        return create_report(
            manager,
            expressions=expressions,
            report_category=report_category,
            setup_name=setup_name,
            variations=variations,
            context=context,
            report_name=report_name,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_create_field_plot(
    plot_kind: Literal["surface", "cutplane", "cut_plane", "volume"],
    assignment: str | list[str],
    quantity: str,
    setup: str | None = None,
    intrinsics: str | dict[str, str] | None = None,
    plot_name: str | None = None,
    field_type: str = "DC R/L Fields",
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a field plot through the active post processor."""
    with manager.locked():
        return create_field_plot(
            manager,
            plot_kind=plot_kind,
            assignment=assignment,
            quantity=quantity,
            setup=setup,
            intrinsics=intrinsics,
            plot_name=plot_name,
            field_type=field_type,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_get_solution_data(
    expressions: str | list[str],
    setup_name: str | None = None,
    variations: dict[str, Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Get solution data from the active AEDT design."""
    with manager.locked():
        return get_solution_data(
            manager,
            expressions=expressions,
            setup_name=setup_name,
            variations=variations,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_export_report(
    report_name: str,
    output_path: str,
    file_format: str = "csv",
) -> dict[str, Any]:
    """Export an AEDT report to a file."""
    with manager.locked():
        return export_report(
            manager,
            report_name=report_name,
            output_path=output_path,
            file_format=file_format,
        )


@mcp.tool()
def aedt_export_field_plot(
    plot_name: str,
    output_dir: str,
    file_name: str = "",
    file_format: str = "aedtplt",
) -> dict[str, Any]:
    """Export a named AEDT field plot."""
    with manager.locked():
        return export_field_plot(
            manager,
            plot_name=plot_name,
            output_dir=output_dir,
            file_name=file_name,
            file_format=file_format,
        )


@mcp.tool()
def aedt_export_app_data(
    export_kind: Literal[
        "3d_model",
        "antenna_metadata",
        "convergence",
        "design_preview",
        "element_pattern",
        "mesh_stats",
        "parametric_results",
        "profile",
        "results",
        "touchstone",
        "variables",
    ],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Export common AEDT design artifacts through PyAEDT export methods."""
    with manager.locked():
        return export_app_data(manager, export_kind=export_kind, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_native_module_call(
    module_name: str,
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call a method on an AEDT native module returned by odesign.GetModule(module_name)."""
    with manager.locked():
        return native_module_call(
            manager,
            module_name=module_name,
            method=method,
            args=args,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_run_app_method(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call a public method on the active PyAEDT app object."""
    with manager.locked():
        return run_app_method(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_list_api(
    target: Literal[
        "app",
        "desktop",
        "modeler",
        "post",
        "mesh",
        "materials",
        "variable_manager",
        "parametrics",
        "optimizations",
        "setups",
        "boundaries",
        "configurations",
        "odesktop",
        "oproject",
        "odesign",
        "oeditor",
        "omodule",
    ] = "app",
    module_name: str | None = None,
    include_private: bool = False,
) -> dict[str, Any]:
    """List public methods and attributes on a PyAEDT or native AEDT object."""
    with manager.locked():
        obj = manager.target(target, module_name=module_name)
        return list_api(obj, include_private=include_private)


@mcp.tool()
def aedt_call(
    target: Literal[
        "app",
        "desktop",
        "modeler",
        "post",
        "mesh",
        "materials",
        "variable_manager",
        "parametrics",
        "optimizations",
        "setups",
        "boundaries",
        "configurations",
        "odesktop",
        "oproject",
        "odesign",
        "oeditor",
        "omodule",
    ],
    attr_path: str | list[str] | None = None,
    method: str | None = None,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
    module_name: str | None = None,
    allow_private: bool = False,
) -> dict[str, Any]:
    """Invoke a public PyAEDT or AEDT native method for broad AEDT API coverage."""
    with manager.locked():
        obj = manager.target(target, module_name=module_name)
        result = invoke(
            obj,
            attr_path=attr_path,
            method=method,
            args=args,
            kwargs=kwargs,
            allow_private=allow_private,
        )
        return {"result": to_jsonable(result)}


@mcp.resource("aedt://session")
def aedt_session_resource() -> dict[str, Any]:
    """Current AEDT session state."""
    return manager.info()


@mcp.resource("aedt://capabilities")
def aedt_capabilities_resource() -> dict[str, Any]:
    """Server capability summary."""
    return {
        "dedicated_tools": [
            "aedt_environment",
            "aedt_start_session",
            "aedt_open_project",
            "aedt_save_project",
            "aedt_list_projects",
            "aedt_new_project",
            "aedt_insert_design",
            "aedt_set_active_project",
            "aedt_set_active_design",
            "aedt_design_summary",
            "aedt_set_variable",
            "aedt_get_variables",
            "aedt_create_dataset",
            "aedt_import_dataset",
            "aedt_create_geometry",
            "aedt_assign_material",
            "aedt_assign_boundary_or_excitation",
            "aedt_mesh_operation",
            "aedt_create_setup",
            "aedt_create_parametric_sweep",
            "aedt_create_optimization",
            "aedt_analyze",
            "aedt_create_report",
            "aedt_create_field_plot",
            "aedt_get_solution_data",
            "aedt_export_report",
            "aedt_export_field_plot",
            "aedt_export_app_data",
            "aedt_native_module_call",
        ],
        "broad_bridge_tools": ["aedt_list_api", "aedt_call", "aedt_run_app_method"],
        "native_targets": ["odesktop", "oproject", "odesign", "oeditor", "omodule"],
    }


@mcp.prompt()
def aedt_workflow_prompt(goal: str) -> str:
    """Generate a concise AEDT automation workflow plan for this MCP server."""
    return (
        "Plan an AEDT automation workflow using ansysmcp tools for this goal:\n"
        f"{goal}\n\n"
        "Prefer dedicated tools for common setup/model/simulation/report steps. Use aedt_list_api "
        "and aedt_call when a specific PyAEDT or AEDT native method is needed."
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Ansys Electronics Desktop MCP server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help="MCP transport to use.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
