from abc import ABC, abstractmethod

class AbstractPeople(ABC):
    """Abstract base class for a person."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the full name."""
        raise NotImplementedError

    @abstractmethod
    def get_community_service_hours(self) -> float:
        """Return total community service hours (can be fractional)."""
        raise NotImplementedError
