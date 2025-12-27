import requests

import Person
import People
import Utilities
from dataclasses import dataclass


# API endpoint to get group details
url = Utilities.GROUP_URL

# Defer group initialization until after function definition

def main():
    group = loadGroupFromFile()
    if group is None:
        print("No group data found. Creating empty group...")
        group = People.People(name="Default Group", members=[])
    # ...rest of your main routine...

if __name__ == "__main__":
    main()




# Checks a group of people and adds in anyone in the GroupMe that isn't in the group
def listOfMembers(self):
    # Use the existing Person class

    # Make the request
    response = requests.get(url)

    people = []
    if response.status_code == 200:
        group_data = response.json()
        members = group_data.get('response', {}).get('members', [])

        for member in members:
            people.append(Person(
                name=member.get('nickname'),
                community_hours=0  # Defaulting community hours to 0
            ))

        return people
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


def sendMessage(self, text):
    payload = {
        "bot_id": Utilities.BOT_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    if response.status_code == 202:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")



def saveGroup(People):
        filename = "group_members.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                count = 0
                for p in People:
                    f.write(f"{p.get_name()}\t{p.get_community_service_hours()}\n")
                    count += 1
            print(f"Saved {count} members to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save group: {e}")
            return False


def loadGroupFromFile():
    """
    Load a People object from the text file specified in Utilities.SAVE_FILE_NAME.
    This function should be called on start to load existing group data.

    Returns:
        A People object if successful, None otherwise.
    """
    filename = Utilities.SAVE_FILE_NAME
    group = People.People.load_from_file(filename)
    return group


def print_help():
    """Print available commands."""
    print("\n" + "=" * 60)
    print("Available Commands:")
    print("=" * 60)
    print("  view all          - View all members and their community hours")
    print("  view below        - View members below the required hours goal")
    print("  reset             - Reset all members' community hours to 0")
    print("  save              - Save current group data to file")
    print("  help              - Show this help message")
    print("  exit / quit       - Exit the program")
    print("=" * 60 + "\n")


def view_all_members(group):
    """Display all members and their community service hours."""
    members = group.get_members()
    if not members:
        print("No members found.")
        return

    print("\n" + "=" * 60)
    print(f"All Members ({len(members)} total):")
    print("=" * 60)
    print(f"{'Name':<40} {'Hours':<10}")
    print("-" * 60)

    for member in members:
        name = member.get_name()
        hours = member.get_community_service_hours()
        print(f"{name:<40} {hours:<10}")

    print("=" * 60 + "\n")


def view_members_below_goal(group):
    """Display members who haven't reached the required community hours."""
    required_hours = Utilities.REQUIRED_COMMUNITY_HOURS
    below_goal = group.get_members_below_goal(required_hours)

    if not below_goal:
        print(f"\nAll members have reached the required {required_hours} hours!\n")
        return

    print("\n" + "=" * 60)
    print(f"Members Below Goal ({required_hours} hours required):")
    print("=" * 60)
    print(f"{'Name':<40} {'Hours':<10} {'Needed':<10}")
    print("-" * 60)

    for member in below_goal:
        name = member.get_name()
        hours = member.get_community_service_hours()
        needed = required_hours - hours
        print(f"{name:<40} {hours:<10} {needed:<10.1f}")

    print("=" * 60 + "\n")


def reset_community_hours(group):
    """Reset all members' community service hours to 0."""
    count = group.reset_all_community_hours()
    print(f"\nReset community hours for {count} member(s).\n")


def save_group(group):
    """Save the group to file."""
    filename = Utilities.SAVE_FILE_NAME
    if group.save_to_file(filename):
        print(f"\nGroup saved successfully to {filename}\n")
    else:
        print(f"\nFailed to save group to {filename}\n")


def main():
    """Main command-line interface loop."""
    print("=" * 60)
    print("GroupMe Helper - Community Hours Manager")
    print("=" * 60)

    # Load group from file on start
    print(f"\nLoading group from {Utilities.SAVE_FILE_NAME}...")
    group = loadGroupFromFile()

    if group is None:
        print("No group data found. Creating empty group...")
        group = People.People(name="Default Group", members=[])

    print(f"Group loaded: {group.get_name()}")
    print(f"Members: {len(group.get_members())}")
    print(f"Required hours: {Utilities.REQUIRED_COMMUNITY_HOURS}")

    print_help()

    # Command loop
    while True:
        try:
            command = input("Enter command (type 'help' for options): ").strip().lower()

            if command in ['exit', 'quit', 'q']:
                # Ask if user wants to save before exiting
                save_choice = input("Save changes before exiting? (y/n): ").strip().lower()
                if save_choice == 'y':
                    save_group(group)
                print("Goodbye!")
                break

            elif command in ['view all', 'viewall', 'list', 'all']:
                view_all_members(group)

            elif command in ['view below', 'viewbelow', 'below', 'incomplete']:
                view_members_below_goal(group)

            elif command in ['reset', 'reset hours', 'resetall']:
                confirm = input("Are you sure you want to reset all community hours? (y/n): ").strip().lower()
                if confirm == 'y':
                    reset_community_hours(group)
                    save_choice = input("Save changes? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        save_group(group)
                else:
                    print("Reset cancelled.\n")

            elif command in ['save', 's']:
                save_group(group)

            elif command in ['help', 'h', '?']:
                print_help()

            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            save_choice = input("Save changes before exiting? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_group(group)
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
