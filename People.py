from typing import Iterable, Any
import AbstractPeople
import Person


class People(AbstractPeople):
    """
    A group of people. Expects `members` to be an iterable of member objects,
    numbers, or dicts. The class implements the abstract methods to return
    the group's name and the total community service hours for all members.
    """

    def __init__(self, name: str, members: Iterable[Any] = ()):
        self._name = name
        # store as list to allow multiple iterations
        self._members = list(members)

    def return_name(self) -> str:
        """Return the group's name."""
        return self._name

    def get_community_service_hours(self):
        return
        