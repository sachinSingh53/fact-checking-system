from fact_checking_system.workflows.system import SystemSmokeWorkflow

WORKFLOWS: list[type] = [SystemSmokeWorkflow]

__all__ = ["WORKFLOWS", "SystemSmokeWorkflow"]
