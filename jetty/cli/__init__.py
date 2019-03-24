import sys

from cleo import Application

from .commands import (
    LockCommand,
)

application = Application()
application.add(LockCommand())


def run():
    application.run()


if __name__ == '__main__':
    sys.exit(run())
