# Roadmap

## Near Term

- Add verified examples for Desktop/native workflows.
- Add focused wrappers for common native modules:
  - `AnalysisSetup`
  - `BoundarySetup`
  - `ReportSetup`
  - `Optimetrics`
  - `FieldsReporter`
- Expand solver-specific allowlists for AEDT actions that PyAEDT exposes across HFSS, Maxwell, Q3D, Icepak, and Circuit.
- Add sample MCP prompts for geometry creation, parametric sweeps, and report export.
- Generate a machine-readable API map from installed PyAEDT classes.

## Solver Workflows

- HFSS: variables, 3D primitives, materials, ports, setup, sweep, S-parameter reports, Touchstone data, and near-field extraction.
- Maxwell 3D: geometry, coils, excitations, solve setup, loss reports.
- Q3D/Q2D: nets, sources/sinks, matrix extraction, capacitance/inductance exports.
- Icepak: thermal setup, power maps, monitor points, monitor data, and temperature reports.
- Circuit: schematic components, Nexxim setup, S-parameter export.

## Release Quality

- Add integration smoke scripts gated by local AEDT availability.
- Add sample `.aedt` artifact generation recipes.
- Add docs site with English and Simplified Chinese pages.
- Add versioned compatibility matrix for AEDT and PyAEDT releases.

## Community Growth

- Keep SEO-focused README copy updated.
- Publish issue templates for solver workflow requests.
- Add example galleries for reproducible non-commercial projects.
- Maintain GitHub topics for Ansys, AEDT, PyAEDT, MCP, HFSS, Maxwell, Q3D, Icepak, CAE, EDA, and AI agents.
