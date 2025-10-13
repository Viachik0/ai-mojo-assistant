import pytest
from app.services.analysis_service import AnalysisService
from app.integrations.mojo_client import MojoClient

@pytest.mark.asyncio
async def test_analysis_service():
    client = MojoClient("", "")
    service = AnalysisService(client)
    # Add actual tests
    assert service is not None