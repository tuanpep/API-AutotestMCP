import os
import json
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from mcp.server.fastmcp import FastMCP

from .config import settings
from .models import CLIENT_PROFILES, SessionReport
from .logic import execute_request, request_logs
from .utils import ensure_dirs, parse_curl_command

# Initialize FastMCP Server
mcp = FastMCP("api-tester")

@mcp.tool()
async def simulate_client_request(
    url: str,
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
    client_type: Literal["iphone_app", "android_app", "chrome_desktop", "safari_mac"],
    payload: Optional[Dict[str, Any]] = None,
    auth_token: Optional[str] = None
) -> str:
    """
    Execute a request simulating a specific client device (iPhone, Android, Chrome/Safari Desktop).
    - url: Full URL including protocol
    - method: HTTP method
    - client_type: The device profile to use
    - payload: Optional JSON body
    - auth_token: Optional Bearer token
    """
    profile = CLIENT_PROFILES.get(client_type, {})
    headers = profile.copy()
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    if payload:
        headers["Content-Type"] = "application/json"

    return await execute_request(
        url=url, 
        method=method, 
        headers=headers, 
        data=payload, 
        client_type=client_type
    )

@mcp.tool()
async def run_curl(command: str) -> str:
    """
    Execute a raw curl command. 
    Useful for complex headers, cookies, or copied commands from DevTools.
    Supports Windows CMD caret (^) escaping.
    """
    try:
        parsed = parse_curl_command(command)
        if not parsed["url"]:
            return "Error: Could not extract URL from curl command."
        
        # Determine client type
        client_type = "curl_custom"
        
        return await execute_request(
            url=parsed["url"],
            method=parsed["method"],
            headers=parsed["headers"],
            data=parsed["data"],
            cookies=parsed["cookies"],
            client_type=client_type
        )
    except Exception as e:
        return f"Error processing curl command: {str(e)}"

@mcp.tool()
def export_test_report(
    session_id: str,
    format: Literal["json", "markdown"] = "markdown"
) -> str:
    """
    Export all requests in the current session to a single report file.
    - session_id: A unique identifier for the report file
    - format: 'json' or 'markdown'
    """
    ensure_dirs()
    
    filename = f"{session_id}.{format}"
    filepath = os.path.join(settings.resolved_exports_dir, filename)
    abs_filepath = os.path.abspath(filepath)
    
    if format == "json":
        report = SessionReport(
            session_id=session_id,
            total_requests=len(request_logs),
            requests=request_logs
        )
        with open(filepath, "w") as f:
            f.write(report.model_dump_json(indent=2))
            
    elif format == "markdown":
        content = f"# Test Report: {session_id}\n"
        content += f"**Date:** {datetime.now().isoformat()}\n"
        content += f"**Total Requests:** {len(request_logs)}\n\n"
        content += "---\n"
        
        for idx, entry in enumerate(request_logs, 1):
            perf_icon = "⚠️" if entry.performance_warning else "✅"
            content += f"## {idx}. {entry.method} {entry.url}\n"
            content += f"- **Status:** {entry.response.status_code if entry.response.status_code else 'ERROR'}\n"
            content += f"- **Client:** `{entry.client_type}`\n"
            content += f"- **Time:** {entry.duration_ms}ms {perf_icon}\n"
            
            if entry.request_payload:
                content += "### Request Payload\n"
                content += "```json\n"
                content += json.dumps(entry.request_payload, indent=2)
                content += "\n```\n"

            if entry.response.error:
                 content += f"- **Error:** {entry.response.error}\n"
            else:
                content += "### Response Snippet\n"
                content += "```json\n"
                if entry.response.json_data:
                    content += json.dumps(entry.response.json_data, indent=2)
                else:
                    content += entry.response.text or ""
                content += "\n```\n"
            content += "\n---\n"
            
        with open(filepath, "w") as f:
            f.write(content)
    
    return f"Report exported successfully to {abs_filepath}"

def main():
    ensure_dirs()
    mcp.run()

if __name__ == "__main__":
    main()
