from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

ClientType = Literal["iphone_app", "android_app", "chrome_desktop", "safari_mac", "curl_custom"]

class ResponseCapture(BaseModel):
    status_code: Optional[int] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    text: Optional[str] = None
    json_data: Optional[Any] = Field(default=None, alias="json")
    size_bytes: int = 0
    error: Optional[str] = None

class RequestLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    url: str
    method: str
    client_type: str
    request_payload: Optional[Any] = None
    request_headers: Dict[str, str] = Field(default_factory=dict)
    response: ResponseCapture
    duration_ms: float
    performance_warning: bool = False

class SessionReport(BaseModel):
    session_id: str
    generated_at: datetime = Field(default_factory=datetime.now)
    total_requests: int
    requests: List[RequestLogEntry]

CLIENT_PROFILES: Dict[str, Dict[str, str]] = {
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
