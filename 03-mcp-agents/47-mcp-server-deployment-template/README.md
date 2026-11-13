# MCP server deployment template

A minimal container template for a Python MCP server using stdio transport. The image runs as a non-root user, installs pinned-at-build dependency constraints from the project metadata, and uses a small runtime command.

## Build and run
```bash
docker build -t mcp-server-template .
docker run --rm -i --read-only --cap-drop=ALL --security-opt=no-new-privileges mcp-server-template
```

## Production checklist
- Use a reviewed base-image digest and lock dependencies.
- Mount only required filesystems; keep root filesystem read-only.
- Provide secrets through an orchestrator secret manager.
- Apply CPU/memory/PID limits and egress allowlists.
- Configure transport authentication at the hosting boundary.
- Run vulnerability scanning and rebuild regularly.

This is a packaging starting point, not a complete production deployment. Stdio servers are typically supervised by an MCP host; expose them only through an explicitly designed transport gateway.
