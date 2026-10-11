"""
McDonald's China Streamable HTTP MCP Client.
Connects to https://mcp.mcd.cn using standard Model Context Protocol streamable HTTP format.
"""
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

DEFAULT_ENDPOINT = "https://mcp.mcd.cn"

class McDonaldMCPClient:
    def __init__(self, token: Optional[str] = None, endpoint: str = DEFAULT_ENDPOINT):
        self.token = token or os.getenv("MCD_MCP_TOKEN", "")
        self.endpoint = endpoint.rstrip("/")

    @property
    def is_configured(self) -> bool:
        return bool(self.token and self.token != "YOUR_MCP_TOKEN")

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invokes an MCP tool on the McDonald's MCP server.
        """
        if not self.is_configured:
            return {
                "success": False,
                "error": "MCD_MCP_TOKEN is not configured. Running in offline/fallback mock mode.",
                "code": 401
            }

        url = f"{self.endpoint}/v1/tools/call"
        payload = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        data = json.dumps(payload).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "McFit-Agent/1.0.0"
        }

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_text = resp.read().decode("utf-8")
                return {
                    "success": True,
                    "data": json.loads(resp_text)
                }
        except urllib.error.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP Error {e.code}: {e.reason}",
                "code": e.code
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": -1
            }
