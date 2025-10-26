import AbstractPeople

class Person(AbstractPeople):
    def __init__(self, name: str, community_hours: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if not isinstance(community_hours, int) or community_hours < 0:
            raise ValueError("Age must be a non-negative integer.")

        self.name = name.strip()
        self.community_hours = community_hours

    # Implement AbstractPeople interface
    def get_name(self) -> str:
        return self.name

    def get_community_service_hours(self) -> int:
        return self.community_hours