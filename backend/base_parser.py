from abc import ABC, abstractmethod

class CodeArtifact(ABC):
    """Abstract base class for all code→document transformers."""

    def __init__(self, py_code: str, filename: str):
        self.py_code = py_code
        self.filename = filename

    @abstractmethod
    def process(self):
        """Subclasses must implement this to perform generation."""
        pass
