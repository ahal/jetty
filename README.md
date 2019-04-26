[![Build Status](https://travis-ci.org/ahal/jetty.svg?branch=master)](https://travis-ci.org/ahal/jetty)
[![PyPI version](https://badge.fury.io/py/jetty.svg)](https://badge.fury.io/py/jetty)

# Jetty

Jetty is a *very thin* wrapper around [Poetry][0], the dependency and package management tool.
Unlike Poetry, which assumes you are using it with a package, Jetty is singularly focused on
dependency management. Other than removing all Poetry commands that aren't related to dependency
management, Jetty accomplishes two things:

1. Removes Poetry's requirement to specify a package name, version and description in
   `pyproject.toml`.
2. Provides a programmatic interface to all of the supported commands.

The interface is automatically generated from Poetry's command line definitions. So for example, if
you would normally run:

```shell
$ poetry install --dry-run
```

The equivalent in code becomes:

```python
from jetty import Project
project = Project()
project.install(dry_run=True)
```

Otherwise Jetty shamelessly uses Poetry's logic and commands wholesale.


## FAQ

**When should I consider Jetty?**

There are only a few special circumstances where you might want to consider Jetty:

A. You want to lock dependencies for Python modules that aren't structured as a package. For
example, maybe you are working in a monorepo where modules can be imported across the repo without
the need for packaging.

B. You are developing tools that use dependency locking. Jetty's programmatic API is handy for this
scenario.


**Why not just use Poetry or Pipenv?**

Tools like [Poetry][0] and [Pipenv][1] are really cool and useful for managing your Python packages,
but they assume that you are working with a package. If you are working with a simple python script
or creating tooling for a monorepo, their self imposed workflows fall apart very quickly (or they
don't even work at all).

To be clear, if you *are* working with a Python package and don't need to call these APIs
programmatically, then Jetty doesn't offer you any benefits. Just use Poetry, it is awesome!


**Why not pip-tools?**

Pip-tools is another awesome project, which *does* focus solely on dependency management. But it
still doesn't have a programmatic API, and the UX is a bit less polished than what one might expect
from Poetry or Pipenv. Plus after spending some time looking at both codebases, I saw an easier path
forward for wrapping Poetry.


**Aren't you just packaging up Poetry and passing it off as your own?**

Sort of? Jetty uses Poetry as a dependency without modification, everything is accomplished via
wrapping. In the future, I may attempt to cut out modules that aren't necessary to dependency
management. Depending if this project works out for my use case, I may also attempt to upstream
whatever makes sense.

Poetry is an awesome project that I whole-heartedly recommend and I make no claims for taking
credit.


[0]: https://github.com/sdispater/poetry
[1]: https://github.com/pypa/pipenv
[2]: https://github.com/jazzband/pip-tools
