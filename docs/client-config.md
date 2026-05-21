# MCP Client Configuration

Use this server from an MCP client with `uv`:

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

For HTTP transport:

```powershell
uv run ansys-aedt-mcp --transport streamable-http
```

Recommended first calls:

1. `aedt_environment`
2. `aedt_start_session` with `app_name="desktop"`
3. `aedt_list_projects`
4. `aedt_list_api` with `target="odesktop"`
5. `aedt_call` for exact native AEDT methods
