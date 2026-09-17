from abc import ABC, abstractmethod

from .models import PassEvent


class CaptureBackend(ABC):
    """Common interface every capture method must implement."""

    @abstractmethod
    def capture(self, source_path: str, opt_level: str = "O2") -> list[PassEvent]:
        """source_path: path to .c/.cpp file. opt_level: e.g. "O2". returns: ordered list of PassEvent."""
        raise NotImplementedError