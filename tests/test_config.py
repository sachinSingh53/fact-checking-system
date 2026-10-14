from fact_checking_system.config import Settings


def test_settings_have_safe_local_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.environment == "local"
    assert settings.temporal_namespace == "default"
    assert settings.temporal_task_queue == "fact-checking"
