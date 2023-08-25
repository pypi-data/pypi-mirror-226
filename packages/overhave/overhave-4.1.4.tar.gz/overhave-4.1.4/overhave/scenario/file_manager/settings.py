from pathlib import Path
from typing import Any, Mapping

import httpx
from pydantic import BaseModel, validator

from overhave.base_settings import BaseOverhavePrefix
from overhave.utils import make_url


class EmptyTaskTrackerURLError(ValueError):
    """Exception for situation with empty ```task_tracker_url``` while trying to ```get_task_link```."""


class EmptyGitProjectURLError(ValueError):
    """Exception for situation with empty ```git_project_url``` while trying to ```get_git_feature_url```."""


class OverhaveProjectSettings(BaseOverhavePrefix):
    """
    Entity project settings.

    You could specify your fixture content for specific pytest usage with your own plugins.
    It could give you pretty extended file with powerful possibilities.
    `fixture_context` will be formatted by `OverhaveProccessor` before test would be started.
    """

    # Fixture content in list format, which would be compiled into formatted string.
    fixture_content: list[str] = [
        "from pytest_bdd import scenarios",
        "from overhave import overhave_proxy_manager",
        "pytest_plugins = overhave_proxy_manager().plugin_resolver.get_plugins()",
        "scenarios('{feature_file_path}')",
    ]

    # Task tracker URL
    task_tracker_url: httpx.URL | None
    # Behaviour specification keyword for tasks attachment
    tasks_keyword: str | None

    # Git project URL
    git_project_url: httpx.URL | None

    # Templates are used for creation of test user and system specifications.
    # Keys for specification mapping are still the same - feature types.
    user_spec_template_mapping: Mapping[str, type[BaseModel]] = {}

    @validator("task_tracker_url", pre=True)
    def make_tasktracker_url(cls, v: str | None) -> httpx.URL | None:
        return make_url(v)

    @validator("tasks_keyword")
    def validate_links_keyword(cls, v: str | None, values: dict[str, Any]) -> str | None:
        if isinstance(v, str) and values.get("task_tracker_url") is None:
            raise ValueError("Task tracker URL should be specified in case of links keyword usage!")
        return v

    @validator("git_project_url", pre=True)
    def make_git_project_url(cls, v: str | None) -> httpx.URL | None:
        return make_url(v)

    def get_task_link(self, link: str) -> httpx.URL:
        if isinstance(self.task_tracker_url, httpx.URL):
            return httpx.URL(f"{self.task_tracker_url}/{link}")
        raise EmptyTaskTrackerURLError("Task tracker URL is None, so could not create link URL!")

    def get_git_feature_url(self, filepath: Path) -> httpx.URL:
        if isinstance(self.git_project_url, httpx.URL):
            return httpx.URL(f"{self.git_project_url}/{filepath.as_posix()}")
        raise EmptyGitProjectURLError("Git project URL is None, so could not create link URL!")
