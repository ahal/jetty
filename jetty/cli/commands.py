from cleo import Command

from jetty import lock

class LockCommand(Command):
    """
    Locks the project dependencies.

    lock
    """

    def handle(self):
        self.line("Locking project dependencies...")
        lock()

