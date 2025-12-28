import asyncio
import json
import os
import time
import shlex
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# Initialize FastMCP Server
mcp = FastMCP("api-test-mcp")

# Constants
EXPORTS_DIR = "exports"
PROFILES_DIR = "profiles"

CLIENT_PROFILES = {
    "iphone_app": {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148",
        "X-Client-Type": "iOS-Native"
    },
    "android_app": {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "X-Client-Type": "Android-Native"
    },
    "chrome_desktop": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Client-Type": "Web-Desktop"
    },
    "safari_mac": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "X-Client-Type": "Web-Desktop"
    }
}

# In-memory storage for the current session
request_logs: List[Dict[str, Any]] = []

def ensure_dirs():
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    os.makedirs(PROFILES_DIR, exist_ok=True)

def parse_curl_command(curl_cmd: str) -> Dict[str, Any]:
    """
    Parses a curl command string (including Windows CMD escaping) into a dictionary.
    """
    # 1. Clean up Windows CMD escaping
    # simplistic approach: build a clean string char by char to handle ^ escapes
    final_clean = ""
    i = 0
    while i < len(curl_cmd):
        char = curl_cmd[i]
        if char == '^':
            # Skip the caret and take the next character
            if i + 1 < len(curl_cmd):
                # Check for line continuation (carets followed immediately by newlines)
                if curl_cmd[i+1] == '\n':
                     i += 2
                     continue
                elif curl_cmd[i+1] == '\r' and i+2 < len(curl_cmd) and curl_cmd[i+2] == '\n':
                     i += 3
                     continue
                
                final_clean += curl_cmd[i+1]
                i += 2
            else:
                i += 1
        else:
            final_clean += char
            i += 1
            
    # Fallback cleanup for any missed newlines in unescaped contexts if using shlex
    final_clean = final_clean.replace("\n", " ").replace("\r", " ")

    parsed = {
        "method": "GET",
        "url": "",
        "headers": {},
        "cookies": {},
        "data": None
    }

    try:
        args = shlex.split(final_clean)
    except Exception:
        # Fallback if shlex fails
        args = final_clean.split()
    
    # Filter out 'curl' if present
    if args and args[0] == 'curl':
        args = args[1:]
        
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg.startswith('http'):
            parsed["url"] = arg
        
        elif arg in ['-H', '--header']:
            if i + 1 < len(args):
                header = args[i+1]
                if ':' in header:
                    key, val = header.split(':', 1)
                    parsed["headers"][key.strip()] = val.strip()
                i += 1
        
        elif arg in ['-b', '--cookie']:
            if i + 1 < len(args):
                cookie_str = args[i+1]
                # cookie format: name=val; name2=val2
                for c in cookie_str.split(';'):
                    if '=' in c:
                        k, v = c.split('=', 1)
                        parsed["cookies"][k.strip()] = v.strip()
                i += 1
        
        elif arg in ['-d', '--data', '--data-raw', '--data-ascii', '--data-binary']:
            if i + 1 < len(args):
                parsed["method"] = "POST"
                data_str = args[i+1]
                try:
                    parsed["data"] = json.loads(data_str)
                    if "Content-Type" not in parsed["headers"]:
                        parsed["headers"]["Content-Type"] = "application/json"
                except json.JSONDecodeError:
                    parsed["data"] = data_str
                i += 1
        
        elif arg in ['-X', '--request']:
            if i + 1 < len(args):
                parsed["method"] = args[i+1]
                i += 1
                
        i += 1
        
    return parsed

async def execute_request(url: str, method: str, headers: Dict, data: Any = None, cookies: Dict = None, client_type: str = "custom") -> str:
    start_time = time.time()
    response_data = {}
    error_msg = None
    
    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=data if isinstance(data, dict) else None,
                content=data if isinstance(data, str) else None,
                timeout=30.0
            )
            duration_ms = (time.time() - start_time) * 1000
            
            # Capture Data
            response_data = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "text": response.text[:2000] + ("..." if len(response.text) > 2000 else ""),
                "size_bytes": len(response.content)
            }
            
            try:
                response_data["json"] = response.json()
            except json.JSONDecodeError:
                pass
                
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        error_msg = str(e)
        response_data = {"error": error_msg}

    # Log entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "method": method,
        "client_type": client_type,
        "request_payload": data,
        "request_headers": headers,
        "response": response_data,
        "duration_ms": round(duration_ms, 2),
        "performance_warning": duration_ms > 500
    }
    
    request_logs.append(entry)

    # Output
    status = response_data.get("status_code", "ERROR")
    perf_flag = "⚠️ SLOW" if entry["performance_warning"] else "✅ OK"
    
    output = f"Request to {url} completed.\n"
    output += f"Status: {status}\n"
    output += f"Time: {entry['duration_ms']}ms ({perf_flag})\n"
    if error_msg:
        output += f"Error: {error_msg}\n"
    else:
        output += f"Size: {response_data.get('size_bytes', 0)} bytes\n"
        output += f"Response Preview:\n"
        if "json" in response_data:
            output += json.dumps(response_data["json"], indent=2)
        else:
            output += response_data.get("text", "")
    
    return output

@mcp.tool()
async def simulate_client_request(
    url: str,
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
    client_type: Literal["iphone_app", "android_app", "chrome_desktop", "safari_mac"],
    payload: Optional[Dict[str, Any]] = None,
    auth_token: Optional[str] = None
) -> str:
    """
    Execute a request with specific client profiles.
    """
    # 1. Prepare Headers
    profile = CLIENT_PROFILES.get(client_type, {})
    headers = profile.copy()
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    if payload:
        headers["Content-Type"] = "application/json"

    # 2. Execute
    return await execute_request(url, method, headers, payload, client_type=client_type)

@mcp.tool()
async def run_curl(command: str) -> str:
    """
    Parses and executes a raw curl command.
    """
    try:
        parsed = parse_curl_command(command)
        if not parsed["url"]:
            return "Error: Could not extract URL from curl command."
        
        # Determine client type from headers if possible
        ua = parsed["headers"].get("User-Agent", "curl")
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
    format: Literal["json", "markdown"]
) -> str:
    """
    Package all recent requests into a single test report.
    """
    ensure_dirs()
    
    filename = f"{session_id}.{format}"
    filepath = os.path.join(EXPORTS_DIR, filename)
    
    if format == "json":
        report = {
            "session_id": session_id,
            "generated_at": datetime.now().isoformat(),
            "total_requests": len(request_logs),
            "requests": request_logs
        }
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
            
    elif format == "markdown":
        content = f"# Test Report: {session_id}\n"
        content += f"**Date:** {datetime.now().isoformat()}\n"
        content += f"**Total Requests:** {len(request_logs)}\n\n"
        content += "---\n"
        
        for idx, log in enumerate(request_logs, 1):
            perf_icon = "⚠️" if log["performance_warning"] else "✅"
            content += f"## {idx}. {log['method']} {log['url']}\n"
            content += f"- **Status:** {log['response'].get('status_code', 'N/A')}\n"
            content += f"- **Client:** `{log['client_type']}`\n"
            content += f"- **Time:** {log['duration_ms']}ms {perf_icon}\n"
            content += f"- **Payload:** `{json.dumps(log.get('request_payload'))}`\n"
            
            if "error" in log["response"]:
                content += f"- **Error:** {log['response']['error']}\n"
            else:
                content += f"### Response Snippet\n"
                content += "```json\n"
                # Try to pretty print json if available
                res_json = log["response"].get("json")
                if res_json:
                    content += json.dumps(res_json, indent=2)
                else:
                    content += log["response"].get("text", "")
                content += "\n```\n"
            content += "\n---\n"
            
        with open(filepath, "w") as f:
            f.write(content)
    
    return f"Report exported successfully to {filepath}"

def main():
    ensure_dirs()
    mcp.run()

if __name__ == "__main__":
    main()
