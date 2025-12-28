import pytest
from api_test_mcp.utils import parse_curl_command

def test_parse_basic_curl():
    cmd = "curl https://example.com"
    parsed = parse_curl_command(cmd)
    assert parsed["url"] == "https://example.com"
    assert parsed["method"] == "GET"

def test_parse_curl_with_headers():
    cmd = 'curl -H "Authorization: Bearer test" -H "X-Custom: val" https://api.com'
    parsed = parse_curl_command(cmd)
    assert parsed["url"] == "https://api.com"
    assert parsed["headers"]["Authorization"] == "Bearer test"
    assert parsed["headers"]["X-Custom"] == "val"

def test_parse_curl_post_data():
    cmd = "curl -X POST -d '{\"key\": \"value\"}' https://api.com"
    parsed = parse_curl_command(cmd)
    assert parsed["method"] == "POST"
    assert parsed["data"] == {"key": "value"}
    assert parsed["headers"]["Content-Type"] == "application/json"

def test_parse_curl_windows_escaping():
    cmd = 'curl ^\n  -H "X-Key: 123" ^\n  "https://api.com"'
    parsed = parse_curl_command(cmd)
    assert parsed["url"] == "https://api.com"
    assert parsed["headers"]["X-Key"] == "123"

def test_parse_curl_no_prefix():
    cmd = "https://example.com -X GET"
    parsed = parse_curl_command(cmd)
    assert parsed["url"] == "https://example.com"
    assert parsed["method"] == "GET"
