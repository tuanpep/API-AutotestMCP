import os
import json
import shlex
import re
from typing import Any, Dict, List, Optional
from .config import settings

def ensure_dirs():
    """Ensures that required directories exist."""
    os.makedirs(settings.resolved_exports_dir, exist_ok=True)
    os.makedirs(settings.resolved_profiles_dir, exist_ok=True)

def parse_curl_command(curl_cmd: str) -> Dict[str, Any]:
    """
    Parses a curl command string into a structured dictionary.
    Handles Windows CMD escaping and basic curl flags.
    """
    # 1. Clean up Windows CMD escaping (carets)
    final_clean = ""
    i = 0
    while i < len(curl_cmd):
        char = curl_cmd[i]
        if char == '^':
            if i + 1 < len(curl_cmd):
                # Check for line continuation
                if curl_cmd[i+1] in ['\n', '\r']:
                    if curl_cmd[i+1] == '\r' and i+2 < len(curl_cmd) and curl_cmd[i+2] == '\n':
                        i += 3
                    else:
                        i += 2
                    continue
                final_clean += curl_cmd[i+1]
                i += 2
            else:
                i += 1
        else:
            final_clean += char
            i += 1
            
    # Remove obvious newlines that might break shlex
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
        args = final_clean.split()
    
    if args and args[0].lower() == 'curl':
        args = args[1:]
        
    i = 0
    while i < len(args):
        arg = args[i]
        
        # URL detection (improved)
        if not parsed["url"] and (re.match(r'^https?://', arg) or not arg.startswith('-')):
             # Sometimes the URL is just sitting there without a flag
             if not arg.startswith('-'):
                parsed["url"] = arg
        
        if arg in ['-H', '--header']:
            if i + 1 < len(args):
                header = args[i+1]
                if ':' in header:
                    key, val = header.split(':', 1)
                    parsed["headers"][key.strip()] = val.strip()
                i += 1
        
        elif arg in ['-b', '--cookie']:
            if i + 1 < len(args):
                cookie_str = args[i+1]
                for c in cookie_str.split(';'):
                    if '=' in c:
                        k, v = c.split('=', 1)
                        parsed["cookies"][k.strip()] = v.strip()
                i += 1
        
        elif arg in ['-d', '--data', '--data-raw', '--data-ascii', '--data-binary']:
            if i + 1 < len(args):
                if parsed["method"] == "GET":
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
                parsed["method"] = args[i+1].upper()
                i += 1
                
        i += 1
        
    return parsed
