import sys

from jetty.cli.application import Application


def run():
    Application().run()


if __name__ == '__main__':
    sys.exit(run())
