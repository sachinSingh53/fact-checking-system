from temporalio import workflow


@workflow.defn
class SystemSmokeWorkflow:
    """Infrastructure-only workflow used to prove worker connectivity."""

    @workflow.run
    async def run(self, value: str) -> str:
        return value
