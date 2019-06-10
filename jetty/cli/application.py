from __future__ import absolute_import

from cleo import Application as BaseApplication
from cleo.formatters import Formatter
from poetry.console.application import Application as PoetryApplication
from poetry.console.commands import (
    AddCommand,
    InstallCommand,
    LockCommand,
    RemoveCommand,
    ShowCommand,
    UpdateCommand,
)

from jetty.__version__ import __version__
from jetty.project import JettisonedPoetry


class Application(PoetryApplication):

    def __init__(self, path=None):
        BaseApplication.__init__(self, "Jetty", __version__)
        self._path = path
        self._poetry = None
        self._skip_io_configuration = False
        self._formatter = Formatter(True)
        self._formatter.add_style("error", "red", options=["bold"])

    @property
    def poetry(self):
        if self._poetry:
            return self._poetry

        self._poetry = JettisonedPoetry.create(self._path)
        return self._poetry

    def get_default_commands(self):
        commands = BaseApplication.get_default_commands(self)

        commands += [
            AddCommand(),
            RemoveCommand(),
            InstallCommand(),
            LockCommand(),
            ShowCommand(),
            UpdateCommand(),
        ]

        return commands
