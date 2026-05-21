<div align="center">

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

SEO 关键词：Ansys MCP、AEDT MCP server、Ansys Electronics Desktop 自动化、PyAEDT MCP、HFSS 自动化、Maxwell 自动化、Q3D 自动化、Icepak 自动化、AI 仿真 Agent、电磁仿真自动化、EDA Agent 工具、CAE 自动化。

## 核心能力

- **MCP 原生支持：** 基于官方 Python MCP SDK，支持 stdio、SSE、streamable HTTP。
- **PyAEDT 优先：** 覆盖 HFSS、Maxwell、Q3D/Q2D、Icepak、Circuit、Twin Builder、EMIT、RMxprt、Mechanical、HFSS 3D Layout。
- **AEDT 原生桥：** 可访问 `odesktop`、`oproject`、`odesign`、`oeditor` 和 `odesign.GetModule(...)`。
- **仿真流程工具：** 变量、数据集、几何、材料、setup、参数扫描、优化、分析、报告、场图和导出。
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
| 环境 | `aedt_environment` |
| 会话 | `aedt_start_session`, `aedt_release_session`, `aedt_session_info` |
| 项目与设计 | `aedt_open_project`, `aedt_save_project`, `aedt_list_projects`, `aedt_new_project`, `aedt_insert_design` |
| 变量与数据集 | `aedt_set_variable`, `aedt_get_variables`, `aedt_create_dataset`, `aedt_import_dataset` |
| 建模与材料 | `aedt_create_geometry`, `aedt_assign_material` |
| 仿真 | `aedt_create_setup`, `aedt_analyze` |
| 探索 | `aedt_create_parametric_sweep`, `aedt_create_optimization` |
| 后处理 | `aedt_create_report`, `aedt_create_field_plot`, `aedt_get_solution_data` |
| 导出 | `aedt_export_report`, `aedt_export_field_plot`, `aedt_export_app_data` |
| 广覆盖 API | `aedt_run_app_method`, `aedt_list_api`, `aedt_call` |

当前 MCP 注册工具数：**28**。

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
- `pytest` 13 个用例通过
- MCP 注册 28 个工具
- AEDT 2024 R2 Desktop/native 烟测通过

## 许可

项目采用 [PolyForm Noncommercial License 1.0.0](LICENSE.md)。

商业授权与再分发权限需要单独书面协议。
