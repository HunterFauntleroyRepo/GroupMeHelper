from typing import Iterable, Any, Optional
from AbstractPeople import AbstractPeople
import Person


class People(AbstractPeople):
    """
    A group of people. Expects `members` to be an iterable of member objects,
    numbers, or dicts. The class implements the abstract methods to return
    the group's name and the total community service hours for all members.
    """

    def __init__(self, name: str, members: Iterable[Person.Person] = ()):
        self._name = name
        # store as list to allow multiple iterations
        self._members = list[Person.Person](members)


    def get_name(self) -> str:
        """Return the group's name (required by AbstractPeople)."""
        return self._name

    def get_community_service_hours(self) -> float:
        """Return total community service hours for all members."""
        total = 0.0
        for member in self._members:
            if hasattr(member, 'get_community_service_hours'):
                hours = member.get_community_service_hours()
                if isinstance(hours, (int, float)):
                    total += float(hours)
        return total

    def get_members(self):
        """Return the list of members."""
        return self._members

    def get_members_below_goal(self, required_hours: float):
        """
        Return members who haven't reached the required community service hours.

        Args:
            required_hours: The minimum required community service hours.

        Returns:
            List of Person objects below the goal.
        """
        below_goal = []
        for member in self._members:
            if hasattr(member, 'get_community_service_hours'):
                hours = member.get_community_service_hours()
                if hours < required_hours:
                    below_goal.append(member)
        return below_goal

    def reset_all_community_hours(self):
        """Reset all members' community service hours to 0."""
        for member in self._members:
            if hasattr(member, 'community_hours'):
                member.community_hours = 0
        return len(self._members)

    @classmethod
    def load_from_file(cls, filename: str) -> Optional['People']:
        """
        Load a People object from a text file.

        Args:
            filename: The path to the file to load from.

        Returns:
            A People object if successful, None otherwise.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                print(f"File {filename} is empty")
                return None

            # Parse header to get group name
            group_name = "Unknown Group"
            members = []
            data_started = False

            for line in lines:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Parse header lines
                if line.startswith("Group:"):
                    group_name = line.replace("Group:", "").strip()
                    continue
                elif line.startswith("Total Members:"):
                    continue
                elif line.startswith("-"):
                    data_started = True
                    continue

                # Parse member data (format: name\thours)
                if data_started or "\t" in line:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        try:
                            hours = int(parts[1].strip())
                        except ValueError:
                            # Try float if int fails
                            try:
                                hours = int(float(parts[1].strip()))
                            except ValueError:
                                hours = 0
                        members.append(Person.Person(name=name, community_hours=hours))
                    elif len(parts) == 1 and parts[0].strip():
                        # Handle case where only name is provided
                        name = parts[0].strip()
                        members.append(Person.Person(name=name, community_hours=0))

            if not members:
                print(f"No members found in {filename}")
                return None

            people_obj = cls(name=group_name, members=members)
            print(f"Successfully loaded {len(members)} members from {filename}")
            return people_obj

        except FileNotFoundError:
            print(f"File {filename} not found")
            return None
        except Exception as e:
            print(f"Failed to load People from file: {e}")
            return None

    def save_to_file(self, filename: str = None) -> bool:
        """
        Save the People object's members to a text file.

        Args:
            filename: Optional filename. If not provided, uses the group name with .txt extension.

        Returns:
            True if successful, False otherwise.
        """
        if filename is None:
            # Use group name as filename, sanitize it for filesystem
            filename = f"{self._name.replace(' ', '_').replace('/', '_')}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                # Write header with group name
                f.write(f"Group: {self._name}\n")
                f.write(f"Total Members: {len(self._members)}\n")
                f.write("-" * 50 + "\n\n")

                # Write each member's information
                for member in self._members:
                    # Handle both Person objects and other types
                    if hasattr(member, 'get_name') and hasattr(member, 'get_community_service_hours'):
                        name = member.get_name()
                        hours = member.get_community_service_hours()
                        f.write(f"{name}\t{hours}\n")
                    elif isinstance(member, dict):
                        # Handle dictionary format
                        name = member.get('name', member.get('nickname', 'Unknown'))
                        hours = member.get('community_hours', member.get('community_service_hours', 0))
                        f.write(f"{name}\t{hours}\n")
                    else:
                        # Fallback for other types
                        f.write(f"{str(member)}\n")

            print(f"Successfully saved {len(self._members)} members to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save People to file: {e}")
            return False
