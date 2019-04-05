import os

from poetry import json
from poetry.packages import (
    Locker,
    ProjectPackage,
)
from poetry.poetry import Poetry
from poetry.utils._compat import Path
from poetry.utils.toml_file import TomlFile

from jetty.util.dicttools import merge

here = Path(__file__).parent.resolve()


class Project(Poetry):

    def __init__(self, path=None):
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
        self.check(local_config)

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
        super(Project, self).__init__(pyproject_file, local_config, package, locker)

    @classmethod
    def check(cls, config, strict=False):
        json.SCHEMA_DIR = here / "schemas"
        super(Project, cls).check(config, strict=strict)
