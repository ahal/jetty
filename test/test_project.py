from pathlib import Path

import pytest

from jetty.cli.application import Application
from jetty.project import JettisonedPoetry, Project

here = Path(__file__).parent.resolve()


def test_find_pyproject_file():
    with pytest.raises(RuntimeError):
        JettisonedPoetry.create(here / 'data')

    with pytest.raises(RuntimeError):
        JettisonedPoetry.create(here / 'data' / 'empty' / 'pyproject.toml')

    config_1 = JettisonedPoetry.create(here / 'data' / 'projectA')._local_config
    config_2 = JettisonedPoetry.create(here / 'data' / 'projectA' / 'pyproject.toml')._local_config
    config_3 = JettisonedPoetry.create(here / 'data' / 'projectB')._local_config

    assert config_1 == config_2
    assert config_2 == config_3


def test_api_exists():
    app = Application()
    project = Project(here / 'data' / 'projectA')

    for command in app.get_default_commands():
        assert hasattr(project, command.name)
        assert callable(getattr(project, command.name))
