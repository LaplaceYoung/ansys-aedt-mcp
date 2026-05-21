# Roadmap

## Near Term

- Add verified examples for Desktop/native workflows.
- Add reusable solve-control examples for distributed setup solves, batch solves, solved variations, and profile reads.
- Add reusable runtime-control examples for HPC configurations, license mode, and temporary directories.
- Add project/design maintenance examples for validation, variation listing, settings updates, and design duplication.
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

- HFSS: variables, 3D primitives, materials, ports, setup, sweep, S-parameter reports, Touchstone data/export, near-field extraction, far-field setup, antenna data, and RCS data.
- Maxwell 3D: geometry, coils, excitations, solve setup, loss reports.
- Q3D/Q2D: nets, sources/sinks, object inspection, matrix extraction, capacitance/inductance exports.
- Icepak: thermal setup, power maps, monitor points, monitor data, fan operating points, and temperature reports.
- Circuit: schematic components, Nexxim setup, Touchstone import/reporting, signal-integrity expression lists, and S-parameter export.

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
