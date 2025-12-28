import time
import json
import os
import httpx
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .config import settings
from .models import RequestLogEntry, ResponseCapture, RequestLogEntry, CLIENT_PROFILES
from .utils import ensure_dirs

# In-memory storage for the current session
# We could make this a class but a global list is fine for MCP lifetime
request_logs: List[RequestLogEntry] = []

async def execute_request(
    url: str, 
    method: str, 
    headers: Dict[str, str], 
    data: Any = None, 
    cookies: Dict[str, str] = None, 
    client_type: str = "custom"
) -> str:
    start_time = time.time()
    response_capture = ResponseCapture()
    error_msg = None
    
    try:
        async with httpx.AsyncClient(cookies=cookies, follow_redirects=True) as client:
            # Handle string vs dict data
            json_payload = data if isinstance(data, dict) else None
            content_payload = data if isinstance(data, (str, bytes)) and not isinstance(data, dict) else None
            
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_payload,
                content=content_payload,
                timeout=30.0
            )
            duration_ms = (time.time() - start_time) * 1000
            
            response_capture.status_code = response.status_code
            response_capture.headers = dict(response.headers)
            response_capture.text = response.text[:2000] + ("..." if len(response.text) > 2000 else "")
            response_capture.size_bytes = len(response.content)
            
            try:
                response_capture.json_data = response.json()
            except json.JSONDecodeError:
                pass
                
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        error_msg = str(e)
        response_capture.error = error_msg

    # Log entry
    entry = RequestLogEntry(
        timestamp=datetime.now(),
        url=url,
        method=method,
        client_type=client_type,
        request_payload=data,
        request_headers=headers,
        response=response_capture,
        duration_ms=round(duration_ms, 2),
        performance_warning=duration_ms > 500
    )
    
    request_logs.append(entry)

    # Auto-save request
    try:
        ensure_dirs()
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_url = "".join([c if c.isalnum() else "_" for c in url])[:50]
        filename = f"req_{timestamp_str}_{method}_{safe_url}.json"
        filepath = os.path.join(settings.resolved_exports_dir, filename)
        
        with open(filepath, "w") as f:
            f.write(entry.model_dump_json(indent=2))
            
        save_msg = f"Saved to {filename}"
    except Exception as e:
        save_msg = f"Failed to save: {e}"

    # Build response string
    status = response_capture.status_code or "ERROR"
    perf_flag = "⚠️ SLOW" if entry.performance_warning else "✅ OK"
    
    output = f"Request to {url} completed.\n"
    output += f"Status: {status}\n"
    output += f"Time: {entry.duration_ms}ms ({perf_flag})\n"
    output += f"Export: {save_msg}\n"
    
    if error_msg:
        output += f"Error: {error_msg}\n"
    else:
        output += f"Size: {response_capture.size_bytes} bytes\n"
        output += f"Response Preview:\n"
        if response_capture.json_data:
            output += json.dumps(response_capture.json_data, indent=2)
        else:
            output += response_capture.text or ""
    
    return output
