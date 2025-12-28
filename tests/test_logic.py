import pytest
import respx
from httpx import Response
from api_test_mcp.logic import execute_request, request_logs

@pytest.mark.asyncio
async def test_execute_request_success():
    request_logs.clear()
    with respx.mock:
        respx.get("https://api.test/ok").mock(return_value=Response(200, json={"status": "ok"}))
        
        result = await execute_request(
            url="https://api.test/ok",
            method="GET",
            headers={"User-Agent": "test"},
            client_type="test_util"
        )
        
        assert "Status: 200" in result
        assert len(request_logs) == 1
        assert request_logs[0].response.status_code == 200
        assert request_logs[0].response.json_data == {"status": "ok"}

@pytest.mark.asyncio
async def test_execute_request_failure():
    request_logs.clear()
    with respx.mock:
        respx.get("https://api.test/fail").mock(side_effect=Exception("Connection Error"))
        
        result = await execute_request(
            url="https://api.test/fail",
            method="GET",
            headers={},
            client_type="test_util"
        )
        
        assert "Error: Connection Error" in result
        assert len(request_logs) == 1
        assert request_logs[0].response.error == "Connection Error"
