# Mensa TUD MCP Server

An MCP (Model Context Protocol) server for accessing the TU Dresden canteen API (Studentenwerk Dresden). This server provides tools to query canteen information, available days, and daily meal menus through the OpenMensa v2 API.

You can access it, e.g. via the [jan.ai](https://github.com/janhq/jan) GUI or using [Claude Desktop](https://code.claude.com/docs/en/desktop).

![](docs/images/teaser.png)

## Features

This MCP server provides three tools:

1. **list_canteens** - List all available canteens with their IDs, names, addresses, and coordinates
2. **list_canteen_days** - List all days for which a specific canteen has meal data available
3. **get_meals** - Get all meals available at a specific canteen on a specific date (defaults to today)

## Installation

1. Install [uv](https://github.com/astral-sh/uv) (fast Python package manager)

2. The dependencies will be automatically installed by uv when running the server

### Integrating with GUIs

To use this MCP server e.g. with Claude Desktop, add it to your Claude Desktop configuration file:

**On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the following to your configuration:

```json
{
  "mcpServers": {
    "mensa-tud": {
        "command": "uv",
        "args": [
        "--directory",
        "path\\to\\mensa-tud-mcp",
        "run",
        "server.py"
        ]
    }
  }
}
```

Make sure to adjust the path to match your installation location. In jan.ai you can enter this information under Settings > MCP Servers.

## Under the hood

This server uses the OpenMensa v2 API provided by Studentenwerk Dresden:
- Base URL: `https://api.studentenwerk-dresden.de/openmensa/v2`
- Documentation: [OpenMensa API](https://doc.openmensa.org/api/v2/)

## License

This is a simple MCP server implementation for educational and personal use provided unter MIT License.
