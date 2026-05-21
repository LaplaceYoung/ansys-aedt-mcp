# Circuit Touchstone Workflow

This workflow outlines a Circuit automation path for importing Touchstone data, generating signal-integrity expressions, creating a report, exporting data, and saving the project.

```text
aedt_environment
aedt_start_session(app_name="circuit", version="2024.2", non_graphical=true)
aedt_import_touchstone_solution(input_file="inputs/channel.s4p", solution="Imported_Channel")
aedt_signal_integrity_expressions(drivers=["P1"], receivers=["P3"], excitations=["P1"], math_formula="dB")
aedt_create_touchstone_report(name="Channel Return Loss", curves=["dB(S(1,1))"], solution="Imported_Channel")
aedt_create_report(expressions="dB(S(1,1))", report_name="Imported S11")
aedt_export_report(report_name="Imported S11", output_path="outputs")
aedt_export_touchstone_data(setup="Imported_Channel", output_file="outputs/imported-channel.s4p")
aedt_save_project(project_path="outputs/circuit-touchstone-demo.aedt")
```

Use `aedt_signal_integrity_expressions` before report creation to build return-loss, insertion-loss, NEXT, and FEXT curve lists from ports and nets.
