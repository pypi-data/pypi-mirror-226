from abc import ABC


class File(ABC):

    def read(self):
        raise NotImplementedError(
            'Method read should be implemented in subclass.'
        )

    def path(self):
        raise NotImplementedError(
            'Method path should be implemented in subclass.'
        )
