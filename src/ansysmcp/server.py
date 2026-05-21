from __future__ import annotations

import argparse
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP

from ansysmcp.operations import (
    analyze,
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
    create_geometry,
    create_open_region,
    create_optimization,
    create_output_variable,
    create_parametric_sweep,
    create_port,
    create_report,
    create_setup,
    delete_item,
    design_summary,
    export_app_data,
    export_diagnostics,
    export_field_plot,
    export_icepak_summary,
    export_matrix_data,
    export_report,
    get_evaluated_value,
    get_monitor_data,
    get_nominal_variation,
    get_output_variable,
    get_profile,
    get_setup_properties,
    get_solution_data,
    get_touchstone_data,
    get_traces_for_plot,
    get_variables,
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
    mesh_summary,
    modeler_operation,
    modeler_summary,
    native_change_property,
    native_get_properties,
    native_get_property_value,
    native_module_call,
    new_project,
    optimetrics_setup_operation,
    optimetrics_summary,
    optimization_operation,
    parametric_operation,
    post_operation,
    post_summary,
    project_design_operation,
    q3d_operation,
    read_design_data,
    run_app_method,
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
from ansysmcp.serialization import to_jsonable
from ansysmcp.session import AedtSessionManager, api_manifest, environment_report

mcp = FastMCP("Ansys Electronics Desktop MCP")
manager = AedtSessionManager()


@mcp.tool()
def aedt_environment() -> dict[str, Any]:
    """Inspect Python and PyAEDT availability without launching AEDT."""
    return environment_report()


@mcp.tool()
def aedt_api_manifest(app_name: str | None = None, include_private: bool = False) -> dict[str, Any]:
    """List PyAEDT app constructors and method signatures without launching AEDT."""
    return api_manifest(app_name=app_name, include_private=include_private)


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
def aedt_modeler_summary() -> dict[str, Any]:
    """Return modeler object names, units, coordinate systems, and bounding-box metadata."""
    with manager.locked():
        return modeler_summary(manager)


@mcp.tool()
def aedt_modeler_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted modeler operation for transforms, booleans, sweeps, groups, or regions."""
    with manager.locked():
        return modeler_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_assign_material(assignment: str | list[str], material: str) -> dict[str, Any]:
    """Assign an AEDT material to one object or many objects."""
    with manager.locked():
        return assign_material(manager, assignment=assignment, material=material)


@mcp.tool()
def aedt_materials_summary() -> dict[str, Any]:
    """Return project material keys, material classes, and used materials."""
    with manager.locked():
        return materials_summary(manager)


@mcp.tool()
def aedt_materials_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted materials library operation."""
    with manager.locked():
        return materials_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_material_object_summary(
    assignment: list[Any] | None = None,
    prop_names: str | list[str] | None = None,
) -> dict[str, Any]:
    """Return conductor/dielectric names and object material properties."""
    with manager.locked():
        return material_object_summary(manager, assignment=assignment, prop_names=prop_names)


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
def aedt_hfss_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted HFSS boundary, excitation, RLC, scattering, or source operation."""
    with manager.locked():
        return hfss_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_maxwell_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted Maxwell coil, winding, motion, force, torque, or source operation."""
    with manager.locked():
        return maxwell_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_q3d_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted Q3D/Q2D net, source, sink, thin conductor, or matrix operation."""
    with manager.locked():
        return q3d_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_icepak_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted Icepak thermal source, opening, wall, monitor, fan, or mesh operation."""
    with manager.locked():
        return icepak_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_circuit_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted Circuit schematic, source, Touchstone, or excitation operation."""
    with manager.locked():
        return circuit_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_create_port(
    method: Literal[
        "circuit_port",
        "create_floquet_port",
        "create_spiral_lumped_port",
        "lumped_port",
        "wave_port",
    ],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a common HFSS/Circuit port through a controlled PyAEDT method."""
    with manager.locked():
        return create_port(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_source_port_summary() -> dict[str, Any]:
    """Summarize available ports, sources, and source modes from the active PyAEDT app."""
    with manager.locked():
        return source_port_summary(manager)


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
def aedt_mesh_summary() -> dict[str, Any]:
    """Return mesh operation names, mesh operations, and initial mesh settings."""
    with manager.locked():
        return mesh_summary(manager)


@mcp.tool()
def aedt_create_frequency_sweep(
    sweep_kind: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a frequency sweep, such as linear_count, linear_step, or single_point."""
    with manager.locked():
        return create_frequency_sweep(manager, sweep_kind=sweep_kind, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_create_open_region(
    frequency: str | int | float | None = "1GHz",
    boundary: str = "Radiation",
    apply_infinite_ground: bool = False,
    gp_axis: str = "-z",
) -> dict[str, Any]:
    """Create an HFSS open region around the active model."""
    with manager.locked():
        return create_open_region(
            manager,
            frequency=frequency,
            boundary=boundary,
            apply_infinite_ground=apply_infinite_ground,
            gp_axis=gp_axis,
        )


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
def aedt_setup_summary() -> dict[str, Any]:
    """Return setup names, active setup, nominal sweep, and setup sweep names."""
    with manager.locked():
        return setup_summary(manager)


@mcp.tool()
def aedt_get_setup_properties(name: str) -> dict[str, Any]:
    """Return the PyAEDT setup object summary and its property dictionary."""
    with manager.locked():
        return get_setup_properties(manager, name=name)


@mcp.tool()
def aedt_update_setup(name: str, properties: dict[str, Any]) -> dict[str, Any]:
    """Update an existing AEDT setup property dictionary and call setup.update()."""
    with manager.locked():
        return update_setup(manager, name=name, properties=properties)


@mcp.tool()
def aedt_analyze(setup_name: str | None = None, analyze_all: bool = False) -> dict[str, Any]:
    """Run analysis for a named setup or the active design."""
    with manager.locked():
        return analyze(manager, setup_name=setup_name, analyze_all=analyze_all)


@mcp.tool()
def aedt_analyze_setup(
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
    """Analyze a named setup with PyAEDT distribution and blocking options."""
    with manager.locked():
        return analyze_setup(
            manager,
            name=name,
            cores=cores,
            tasks=tasks,
            gpus=gpus,
            acf_file=acf_file,
            use_auto_settings=use_auto_settings,
            num_variations_to_distribute=num_variations_to_distribute,
            allowed_distribution_types=allowed_distribution_types,
            revert_to_initial_mesh=revert_to_initial_mesh,
            blocking=blocking,
        )


@mcp.tool()
def aedt_solve_in_batch(
    file_name: str | None = None,
    machine: str = "localhost",
    run_in_thread: bool = False,
    cores: int = 4,
    tasks: int = 1,
    setup: str | None = None,
    revert_to_initial_mesh: bool = False,
) -> dict[str, Any]:
    """Launch PyAEDT batch solve for the active design or a named setup."""
    with manager.locked():
        return solve_in_batch(
            manager,
            file_name=file_name,
            machine=machine,
            run_in_thread=run_in_thread,
            cores=cores,
            tasks=tasks,
            setup=setup,
            revert_to_initial_mesh=revert_to_initial_mesh,
        )


@mcp.tool()
def aedt_apply_solved_variation(variation: dict[str, Any]) -> dict[str, Any]:
    """Apply a solved variation dictionary to the active design context."""
    with manager.locked():
        return apply_solved_variation(manager, variation=variation)


@mcp.tool()
def aedt_validate_design(
    validation_kind: Literal["simple", "full"] = "simple",
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run PyAEDT simple or full design validation."""
    with manager.locked():
        return validate_design(
            manager,
            validation_kind=validation_kind,
            args=args,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_cleanup_solution(
    variations: str | list[Any] = "All",
    entire_solution: bool = True,
    field: bool = True,
    mesh: bool = True,
    linked_data: bool = True,
) -> dict[str, Any]:
    """Clean solution data through PyAEDT cleanup_solution options."""
    with manager.locked():
        return cleanup_solution(
            manager,
            variations=variations,
            entire_solution=entire_solution,
            field=field,
            mesh=mesh,
            linked_data=linked_data,
        )


@mcp.tool()
def aedt_change_design_settings(settings: dict[str, Any]) -> dict[str, Any]:
    """Apply active design settings through PyAEDT change_design_settings."""
    with manager.locked():
        return change_design_settings(manager, settings=settings)


@mcp.tool()
def aedt_change_validation_settings(
    entity_check_level: str = "Strict",
    ignore_unclassified: bool = False,
    skip_intersections: bool = False,
) -> dict[str, Any]:
    """Apply active design validation settings."""
    with manager.locked():
        return change_validation_settings(
            manager,
            entity_check_level=entity_check_level,
            ignore_unclassified=ignore_unclassified,
            skip_intersections=skip_intersections,
        )


@mcp.tool()
def aedt_list_variations(
    setup: str | None = None,
    sweep: str | None = None,
) -> dict[str, Any]:
    """List solved or available variation strings for a setup and sweep."""
    with manager.locked():
        return list_variations(manager, setup=setup, sweep=sweep)


@mcp.tool()
def aedt_read_design_data() -> dict[str, Any]:
    """Read PyAEDT design data dictionary for the active design."""
    with manager.locked():
        return read_design_data(manager)


@mcp.tool()
def aedt_project_design_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted project/design maintenance operation."""
    with manager.locked():
        return project_design_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_configuration_summary() -> dict[str, Any]:
    """Return configuration object type and export/import option values."""
    with manager.locked():
        return configuration_summary(manager)


@mcp.tool()
def aedt_configuration_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted configuration import, export, or monitor update operation."""
    with manager.locked():
        return configuration_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_update_configuration_options(
    options: dict[str, Any] | None = None,
    action: Literal[
        "set_all_export",
        "set_all_import",
        "unset_all_export",
        "unset_all_import",
    ]
    | None = None,
) -> dict[str, Any]:
    """Set configuration export/import options or run an all-options action."""
    with manager.locked():
        return update_configuration_options(manager, options=options, action=action)


@mcp.tool()
def aedt_get_nominal_variation(with_values: bool = False) -> dict[str, Any]:
    """Return the nominal variation string or dictionary from the active design."""
    with manager.locked():
        return get_nominal_variation(manager, with_values=with_values)


@mcp.tool()
def aedt_get_evaluated_value(name: str, units: str | None = None) -> dict[str, Any]:
    """Evaluate a variable or expression in the active AEDT design."""
    with manager.locked():
        return get_evaluated_value(manager, name=name, units=units)


@mcp.tool()
def aedt_get_output_variable(variable: str, solution: str | None = None) -> dict[str, Any]:
    """Read a PyAEDT output variable value."""
    with manager.locked():
        return get_output_variable(manager, variable=variable, solution=solution)


@mcp.tool()
def aedt_get_profile(name: str | None = None) -> dict[str, Any]:
    """Return solve profile data for a setup or the active profile context."""
    with manager.locked():
        return get_profile(manager, name=name)


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
def aedt_optimetrics_summary() -> dict[str, Any]:
    """Return parametric and optimization setup names from Optimetrics managers."""
    with manager.locked():
        return optimetrics_summary(manager)


@mcp.tool()
def aedt_parametric_operation(
    method: Literal["add", "add_from_file", "delete"],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted Parametrics manager operation."""
    with manager.locked():
        return parametric_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_optimization_operation(
    method: Literal["add", "delete"],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted Optimizations manager operation."""
    with manager.locked():
        return optimization_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_optimetrics_setup_operation(
    collection: Literal["parametrics", "optimizations"],
    setup_name: str,
    method: Literal["add_calculation", "analyze", "create", "delete", "update"],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted operation on an existing Optimetrics setup."""
    with manager.locked():
        return optimetrics_setup_operation(
            manager,
            collection=collection,
            setup_name=setup_name,
            method=method,
            args=args,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_create_output_variable(
    variable: str,
    expression: str,
    solution: str | None = None,
    context: str | None = None,
) -> dict[str, Any]:
    """Create a PyAEDT output variable for post-processing expressions."""
    with manager.locked():
        return create_output_variable(
            manager,
            variable=variable,
            expression=expression,
            solution=solution,
            context=context,
        )


@mcp.tool()
def aedt_import_cad(
    input_file: str,
    import_kind: str | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Import CAD/layout files through supported PyAEDT import methods."""
    with manager.locked():
        return import_cad(manager, input_file=input_file, import_kind=import_kind, kwargs=kwargs)


@mcp.tool()
def aedt_delete_item(
    method: Literal[
        "delete_design",
        "delete_project",
        "delete_setup",
        "delete_unused_variables",
        "delete_variable",
    ],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Delete selected AEDT items through controlled PyAEDT delete methods."""
    with manager.locked():
        return delete_item(manager, method=method, args=args, kwargs=kwargs)


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
def aedt_get_traces_for_plot(kwargs: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return available report traces from PyAEDT get_traces_for_plot."""
    with manager.locked():
        return get_traces_for_plot(manager, kwargs=kwargs)


@mcp.tool()
def aedt_get_touchstone_data(
    setup: str | None = None,
    sweep: str | None = None,
    variations: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return Touchstone data from the active AEDT design when supported by PyAEDT."""
    with manager.locked():
        return get_touchstone_data(manager, setup=setup, sweep=sweep, variations=variations)


@mcp.tool()
def aedt_get_monitor_data() -> dict[str, Any]:
    """Return monitor data from solvers that expose get_monitor_data."""
    with manager.locked():
        return get_monitor_data(manager)


@mcp.tool()
def aedt_post_summary() -> dict[str, Any]:
    """Return report names, report types, field plots, and available post quantities."""
    with manager.locked():
        return post_summary(manager)


@mcp.tool()
def aedt_post_operation(
    method: str,
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run an allowlisted post-processing operation for reports, fields, plots, or exports."""
    with manager.locked():
        return post_operation(manager, method=method, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_insert_near_field(
    field_kind: Literal["box", "line", "points", "rectangle", "sphere"],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Insert a near-field definition through a controlled PyAEDT helper."""
    with manager.locked():
        return insert_near_field(manager, field_kind=field_kind, args=args, kwargs=kwargs)


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
def aedt_export_diagnostics(
    export_kind: Literal["convergence", "mesh_stats", "profile"],
    setup: str,
    variations: str = "",
    output_file: str | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Export convergence, mesh statistics, or profile diagnostics for a setup."""
    with manager.locked():
        return export_diagnostics(
            manager,
            export_kind=export_kind,
            setup=setup,
            variations=variations,
            output_file=output_file,
            kwargs=kwargs,
        )


@mcp.tool()
def aedt_export_matrix_data(
    export_kind: Literal[
        "maxwell",
        "maxwell_matrix",
        "q3d",
        "q3d_matrix",
        "equivalent_circuit",
        "q3d_equivalent_circuit",
    ],
    args: list[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Export Maxwell/Q3D matrices or Q3D equivalent circuits."""
    with manager.locked():
        return export_matrix_data(manager, export_kind=export_kind, args=args, kwargs=kwargs)


@mcp.tool()
def aedt_export_icepak_summary(
    output_dir: str | None = None,
    solution_name: str | None = None,
    summary_type: str = "Object",
    geometry_type: str = "Volume",
    quantity: str = "Temperature",
    variation: str = "",
    variation_list: list[Any] | None = None,
    filename: str = "IPKsummaryReport",
) -> dict[str, Any]:
    """Export an Icepak summary report for objects, faces, or monitor-style quantities."""
    with manager.locked():
        return export_icepak_summary(
            manager,
            output_dir=output_dir,
            solution_name=solution_name,
            summary_type=summary_type,
            geometry_type=geometry_type,
            quantity=quantity,
            variation=variation,
            variation_list=variation_list,
            filename=filename,
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
def aedt_native_get_properties(
    target: Literal["oproject", "odesign", "oeditor", "omodule"],
    tab: str,
    server: str,
    module_name: str | None = None,
) -> dict[str, Any]:
    """Get AEDT native property names from a target object."""
    with manager.locked():
        return native_get_properties(
            manager,
            target=target,
            tab=tab,
            server=server,
            module_name=module_name,
        )


@mcp.tool()
def aedt_native_get_property_value(
    target: Literal["oproject", "odesign", "oeditor", "omodule"],
    tab: str,
    server: str,
    property_name: str,
    module_name: str | None = None,
) -> dict[str, Any]:
    """Get an AEDT native property value from a target object."""
    with manager.locked():
        return native_get_property_value(
            manager,
            target=target,
            tab=tab,
            server=server,
            property_name=property_name,
            module_name=module_name,
        )


@mcp.tool()
def aedt_native_change_property(
    target: Literal["oproject", "odesign", "oeditor", "omodule"],
    change_payload: list[Any],
    module_name: str | None = None,
) -> dict[str, Any]:
    """Apply an AEDT native ChangeProperty payload to a target object."""
    with manager.locked():
        return native_change_property(
            manager,
            target=target,
            change_payload=change_payload,
            module_name=module_name,
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


@mcp.tool()
def aedt_batch_call(
    operations: list[dict[str, Any]],
    continue_on_error: bool = False,
) -> dict[str, Any]:
    """Execute ordered public PyAEDT/native AEDT calls in one MCP request."""
    with manager.locked():
        return batch_call(
            manager,
            operations=operations,
            continue_on_error=continue_on_error,
        )


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
            "aedt_api_manifest",
            "aedt_start_session",
            "aedt_release_session",
            "aedt_session_info",
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
            "aedt_modeler_summary",
            "aedt_modeler_operation",
            "aedt_assign_material",
            "aedt_materials_summary",
            "aedt_materials_operation",
            "aedt_material_object_summary",
            "aedt_assign_boundary_or_excitation",
            "aedt_hfss_operation",
            "aedt_maxwell_operation",
            "aedt_q3d_operation",
            "aedt_icepak_operation",
            "aedt_circuit_operation",
            "aedt_create_port",
            "aedt_source_port_summary",
            "aedt_mesh_operation",
            "aedt_mesh_summary",
            "aedt_create_setup",
            "aedt_setup_summary",
            "aedt_get_setup_properties",
            "aedt_update_setup",
            "aedt_create_frequency_sweep",
            "aedt_create_open_region",
            "aedt_create_output_variable",
            "aedt_import_cad",
            "aedt_delete_item",
            "aedt_create_parametric_sweep",
            "aedt_optimetrics_summary",
            "aedt_parametric_operation",
            "aedt_optimization_operation",
            "aedt_optimetrics_setup_operation",
            "aedt_create_optimization",
            "aedt_analyze",
            "aedt_analyze_setup",
            "aedt_solve_in_batch",
            "aedt_apply_solved_variation",
            "aedt_validate_design",
            "aedt_cleanup_solution",
            "aedt_change_design_settings",
            "aedt_change_validation_settings",
            "aedt_list_variations",
            "aedt_read_design_data",
            "aedt_project_design_operation",
            "aedt_configuration_summary",
            "aedt_configuration_operation",
            "aedt_update_configuration_options",
            "aedt_get_nominal_variation",
            "aedt_get_evaluated_value",
            "aedt_get_output_variable",
            "aedt_get_profile",
            "aedt_create_report",
            "aedt_create_field_plot",
            "aedt_get_solution_data",
            "aedt_get_traces_for_plot",
            "aedt_get_touchstone_data",
            "aedt_get_monitor_data",
            "aedt_post_summary",
            "aedt_post_operation",
            "aedt_insert_near_field",
            "aedt_export_report",
            "aedt_export_field_plot",
            "aedt_export_diagnostics",
            "aedt_export_matrix_data",
            "aedt_export_icepak_summary",
            "aedt_export_app_data",
            "aedt_native_module_call",
            "aedt_native_get_properties",
            "aedt_native_get_property_value",
            "aedt_native_change_property",
        ],
        "broad_bridge_tools": ["aedt_list_api", "aedt_call", "aedt_run_app_method"],
        "workflow_tools": ["aedt_batch_call"],
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
