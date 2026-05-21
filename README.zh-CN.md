<div align="center">

<img src="assets/logo/ansys-aedt-mcp-logo.png" alt="Ansys AEDT MCP Server logo" width="180">

# Ansys AEDT MCP Server

**面向 Ansys Electronics Desktop、PyAEDT、HFSS、Maxwell、Q3D、Icepak、Circuit、报告、参数扫描和仿真自动化的 MCP 服务器。**

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-compatible-6f42c1)](https://modelcontextprotocol.io/)
[![PyAEDT](https://img.shields.io/badge/PyAEDT-0.26%2B-1793D1)](https://aedt.docs.pyansys.com/)
[![AEDT](https://img.shields.io/badge/Ansys%20Electronics%20Desktop-2024R2%2B-ffb71b)](https://www.ansys.com/products/electronics)
[![License](https://img.shields.io/badge/license-PolyForm--Noncommercial--1.0.0-blue)](LICENSE.md)

[English](README.md) · [简体中文](README.zh-CN.md) · [能力地图](docs/capability-map.md) · [验证记录](docs/verification.md)

</div>

## 项目定位

`ansys-aedt-mcp` 让 AI Agent 和 MCP 客户端通过结构化工具控制 Ansys Electronics Desktop。项目同时提供常用仿真流程的专用工具，以及面向 PyAEDT 和 AEDT 原生对象的广覆盖调用桥。

SEO 关键词：Ansys MCP、AEDT MCP server、Ansys Electronics Desktop 自动化、PyAEDT MCP、HFSS 自动化、HFSS 远场自动化、Touchstone 导出、Touchstone 导入、信号完整性自动化、Maxwell 自动化、Q3D 自动化、Icepak 自动化、AI 仿真 Agent、电磁仿真自动化、EDA Agent 工具、CAE 自动化。

## 核心能力

- **MCP 原生支持：** 基于官方 Python MCP SDK，支持 stdio、SSE、streamable HTTP。
- **PyAEDT 优先：** 覆盖 HFSS、Maxwell、Q3D/Q2D、Icepak、Circuit、Twin Builder、EMIT、RMxprt、Mechanical、HFSS 3D Layout。
- **AEDT 原生桥：** 可访问 `odesktop`、`oproject`、`odesign`、`oeditor` 和 `odesign.GetModule(...)`。
- **仿真流程工具：** 变量、数据集、几何、材料、setup 检查与更新、HPC 配置、参数扫描、优化、分析、报告、场图、远场、天线/RCS 数据、信号完整性表达式、Q3D 网络、Icepak 风扇数据、Touchstone 数据/导入/导出、监控数据和导出。
- **可验证开发：** 单元测试无需 AEDT 授权；Desktop/native 烟测可在已安装 AEDT 的 Windows 机器上运行。
- **非商用源码可用：** 采用 PolyForm Noncommercial 1.0.0，面向研究、教育、个人实验和公共知识场景。

## 快速开始

```powershell
git clone https://github.com/LaplaceYoung/ansys-aedt-mcp.git
cd ansys-aedt-mcp
uv sync --extra dev
uv run ansys-aedt-mcp
```

开发调试：

```powershell
uv run mcp dev src/ansysmcp/server.py
```

HTTP 传输：

```powershell
uv run ansys-aedt-mcp --transport streamable-http
```

## MCP 客户端配置

```json
{
  "mcpServers": {
    "ansys-aedt": {
      "command": "uv",
      "args": ["--directory", "F:\\实验\\ansysmcp", "run", "ansys-aedt-mcp"]
    }
  }
}
```

从 GitHub 克隆后，把路径替换为本机 checkout 路径。

## 工具面

| 领域 | 工具 |
| --- | --- |
| 环境/API 发现 | `aedt_environment`, `aedt_api_manifest` |
| 会话 | `aedt_start_session`, `aedt_release_session`, `aedt_session_info` |
| 项目与设计 | `aedt_open_project`, `aedt_save_project`, `aedt_list_projects`, `aedt_new_project`, `aedt_insert_design`, `aedt_set_active_project`, `aedt_set_active_design`, `aedt_design_summary` |
| 变量与数据集 | `aedt_set_variable`, `aedt_get_variables`, `aedt_create_dataset`, `aedt_import_dataset` |
| 建模与材料 | `aedt_create_geometry`, `aedt_modeler_summary`, `aedt_modeler_operation`, `aedt_assign_material`, `aedt_materials_summary`, `aedt_materials_operation`, `aedt_material_object_summary`, `aedt_mesh_operation`, `aedt_mesh_summary`, `aedt_import_cad` |
| 端口与激励 | `aedt_create_port`, `aedt_source_port_summary`, `aedt_assign_boundary_or_excitation` |
| Solver 专用控制 | `aedt_hfss_operation`, `aedt_maxwell_operation`, `aedt_q3d_operation`, `aedt_q3d_net_summary`, `aedt_icepak_operation`, `aedt_get_fans_operating_point`, `aedt_circuit_operation` |
| 仿真 | `aedt_create_setup`, `aedt_setup_summary`, `aedt_get_setup_properties`, `aedt_update_setup`, `aedt_create_frequency_sweep`, `aedt_create_open_region`, `aedt_analyze`, `aedt_analyze_setup`, `aedt_solve_in_batch`, `aedt_apply_solved_variation`, `aedt_validate_design`, `aedt_cleanup_solution`, `aedt_set_hpc_options`, `aedt_set_license_type`, `aedt_set_temporary_directory`, `aedt_list_variations` |
| 探索 | `aedt_create_parametric_sweep`, `aedt_create_optimization`, `aedt_optimetrics_summary`, `aedt_parametric_operation`, `aedt_optimization_operation`, `aedt_optimetrics_setup_operation` |
| 后处理 | `aedt_create_output_variable`, `aedt_get_output_variable`, `aedt_get_evaluated_value`, `aedt_get_nominal_variation`, `aedt_get_profile`, `aedt_create_report`, `aedt_create_field_plot`, `aedt_get_solution_data`, `aedt_get_traces_for_plot`, `aedt_get_touchstone_data`, `aedt_signal_integrity_expressions`, `aedt_get_monitor_data`, `aedt_insert_far_field`, `aedt_get_antenna_data`, `aedt_get_rcs_data`, `aedt_post_summary`, `aedt_post_operation`, `aedt_insert_near_field`, `aedt_import_touchstone_solution`, `aedt_create_touchstone_report` |
| 导出 | `aedt_export_report`, `aedt_export_touchstone_data`, `aedt_export_field_plot`, `aedt_export_diagnostics`, `aedt_export_matrix_data`, `aedt_export_icepak_summary`, `aedt_export_app_data` |
| 删除 | `aedt_delete_item` |
| 项目与设计维护 | `aedt_change_design_settings`, `aedt_change_validation_settings`, `aedt_edit_design_notes`, `aedt_read_design_data`, `aedt_project_design_operation` |
| 配置 | `aedt_configuration_summary`, `aedt_configuration_operation`, `aedt_update_configuration_options` |
| 原生/OO 属性 | `aedt_native_get_properties`, `aedt_native_get_property_value`, `aedt_native_change_property`, `aedt_oo_object_names`, `aedt_oo_get_properties`, `aedt_oo_get_property_value`, `aedt_oo_set_property_value` |
| 广覆盖 API/工作流 | `aedt_run_app_method`, `aedt_list_api`, `aedt_call`, `aedt_batch_call` |

当前 MCP 注册工具数：**107**。

## 验证命令

```powershell
uv sync --extra dev
uv run ruff check .
uv run pytest
uv run ansys-aedt-mcp --help
uv run python scripts/aedt_smoke.py --mode environment
uv run python scripts/aedt_smoke.py --mode desktop --version 2024.2 --create-project MCPNativeProject
```

当前本地状态：

- `ruff check` 通过
- `pytest` 39 个用例通过
- MCP 注册 107 个工具
- AEDT 2024 R2 Desktop/native 烟测通过

## 示例

- [工作流示例](examples/README.md)

## 许可

项目采用 [PolyForm Noncommercial License 1.0.0](LICENSE.md)。

商业授权与再分发权限需要单独书面协议。
