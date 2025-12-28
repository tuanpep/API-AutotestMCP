import pytest
from api_test_mcp.config import settings

@pytest.fixture(autouse=True)
def setup_test_env(tmp_path):
    """Overrides exports_dir for testing to avoid clutter."""
    test_dir = tmp_path / "test_exports"
    test_dir.mkdir()
    settings.exports_dir = str(test_dir)
    return test_dir
