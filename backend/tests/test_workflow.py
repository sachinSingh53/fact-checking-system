import pytest

from fact_checking_system.workflows.system import SystemSmokeWorkflow


@pytest.mark.asyncio
async def test_system_smoke_workflow_echoes_value() -> None:
    workflow = SystemSmokeWorkflow()

    assert await workflow.run("ok") == "ok"
