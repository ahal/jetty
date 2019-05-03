from __future__ import absolute_import

import os

from cleo.inputs import ArgvInput
from poetry import json
from poetry.packages import (
    Dependency,
    Locker,
    ProjectPackage,
)
from poetry.poetry import Poetry
from poetry.utils._compat import Path
from poetry.utils.toml_file import TomlFile

from jetty.util.dicttools import merge

here = Path(__file__).parent.resolve()


class Project:

    def __init__(self, path=None):
        from jetty.cli import Application
        self._application = Application(path)
        self._poetry = self._application._poetry
        self._application._auto_exit = False
        self._application._poetry = self._poetry

        for name, command in self._application.all().items():
            func = self._make_func(name, command)
            func.__doc__ = command.__doc__
            setattr(self, name, func.__get__(self))

    def _make_func(self, name, command):
        definition = command.get_definition()
        args = []
        kwargs = []

        for arg in definition.get_arguments() + definition.get_options():
            arg_name = arg.get_name().replace("-", "_")

            if hasattr(arg, 'is_required') and arg.is_required():
                args.append(arg_name)
                continue

            arg_default = arg.get_default()
            if isinstance(arg_default, str):
                arg_default = "\"{}\"".format(arg_default)
            kwargs.append("{}={}".format(arg_name, arg_default))

        args = ", ".join(args)
        if args:
            args = ", " + args

        kwargs = ", ".join(kwargs)
        if kwargs:
            kwargs = ", " + kwargs

        exec("""
def {name}(self{args}{kwargs}):
    kwargs = locals().copy()
    del kwargs["self"]
    cmd = self._build_cmd("{name}", **kwargs)
    self._run(["{name}"] + cmd)
""".strip().format(name=name, args=args, kwargs=kwargs))
        return locals()[name]

    def _build_cmd(self, command, **kwargs):
        definition = self._application.all()[command].get_definition()
        cmd = []

        for name, value in kwargs.items():
            name = name.replace("_", "-")

            if definition.has_argument(name):
                arg = definition.get_argument(name)
                if value != arg.get_default():
                    cmd.append(value)

            elif definition.has_option(name):
                opt = definition.get_option(name)
                if value != opt.get_default():
                    if isinstance(value, bool):
                        cmd.append("--{}".format(name))
                    else:
                        cmd.append("--{}={}".format(name, value))

        return cmd

    def _run(self, cmd):
        i = ArgvInput(["poetry -v"] + cmd)
        self._application.run(i)


class JettisonedPoetry(Poetry):

    @classmethod
    def create(cls, path=None):
        path = path or os.getcwd()
        pyproject_file = Path(path)

        if pyproject_file.name != "pyproject.toml":
            pyproject_file = pyproject_file / "pyproject.toml"

        if not pyproject_file.exists():
            raise RuntimeError(
                "Jetty could not find a pyproject.toml file in {}".format(
                    path
                )
            )

        local_config = TomlFile(pyproject_file.as_posix()).read()
        tool = local_config.setdefault('tool', {})

        if 'jetty' not in tool and 'poetry' not in tool:
            raise RuntimeError("[tool.jetty] section not found in {}"
                               .format(pyproject_file.name))

        local_config = merge(tool.get('jetty', {}), tool.get('poetry', {}))

        # Checking validity
        cls.check(local_config)

        # Load package
        name = local_config.get('name', pyproject_file.parent.name)
        version = local_config.get('version', '0')
        package = ProjectPackage(name, version, version)

        if 'dependencies' in local_config:
            for name, constraint in local_config['dependencies'].items():
                if name.lower() == 'python':
                    package.python_versions = constraint
                    continue

                if isinstance(constraint, list):
                    for _constraint in constraint:
                        package.add_dependency(name, _constraint)

                    continue

                package.add_dependency(name, constraint)

        if 'dev-dependencies' in local_config:
            for name, constraint in local_config['dev-dependencies'].items():
                if isinstance(constraint, list):
                    for _constraint in constraint:
                        package.add_dependency(name, _constraint, category='dev')

                    continue

                package.add_dependency(name, constraint, category='dev')

        extras = local_config.get("extras", {})
        for extra_name, requirements in extras.items():
            package.extras[extra_name] = []

            # Checking for dependency
            for req in requirements:
                req = Dependency(req, "*")

                for dep in package.requires:
                    if dep.name == req.name:
                        dep.in_extras.append(extra_name)
                        package.extras[extra_name].append(dep)

                        break

        lock = pyproject_file.parent / "poetry.lock"
        locker = Locker(lock, local_config)
        return cls(pyproject_file, local_config, package, locker)

    @classmethod
    def check(cls, config, strict=False):
        json.SCHEMA_DIR = Path(here / "schemas").as_posix()
        return Poetry.check(config, strict=strict)
