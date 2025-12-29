import requests
import Person
import People
import Utilities
from dataclasses import dataclass


def fetch_groupme_members():
    """Fetch members from GroupMe API → return People.People instance."""
    response = requests.get(Utilities.GROUP_URL)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return People.People(name="Default Group", members=[])
# Parse JSON response
    data = response.json()
    members = data.get("response", {}).get("members", [])
    people = [
        Person.Person(
            name=m.get("nickname"),
            community_hours=0
        ) for m in members
    ]
    return People.People(name="Default Group", members=people)


def load_group_from_file():
    filename = Utilities.SAVE_FILE_NAME
    return People.People.load_from_file(filename)


def save_group(group):
    filename = Utilities.SAVE_FILE_NAME
    if group.save_to_file(filename):
        print(f"\nSaved group to {filename}\n")
    else:
        print("\nFailed to save group\n")


def view_all_members(group):
    members = group.get_members()
    if not members:
        print("No members found.")
        return

    print("\n" + "=" * 60)
    print(f"All Members ({len(members)} total)")
    print("=" * 60)
    print(f"{'Name':<40} {'Hours':<10}")
    print("-" * 60)
    for m in members:
        print(f"{m.get_name():<40} {m.get_community_service_hours():<10}")
    print("=" * 60 + "\n")


def view_members_below_goal(group):
    req = Utilities.REQUIRED_COMMUNITY_HOURS
    below = group.get_members_below_goal(req)
    if not below:
        print(f"\nAll members met the required {req} hours!\n")
        return

    print("\nMembers Below Goal:")
    print("=" * 60)
    for m in below:
        hrs = m.get_community_service_hours()
        needed = req - hrs
        print(f"{m.get_name():<40} {hrs:<10} Need: {needed:<10}")
    print("=" * 60 + "\n")


def reset_community_hours(group):
    cnt = group.reset_all_community_hours()
    print(f"\nReset hours for {cnt} members.\n")


def print_help():
    print("""
============================== Commands ==============================
view all        - View all members
view below      - View members below required hours
reset           - Reset all hours to 0
populate        - Pull GroupMe members + merge into existing group
save            - Save to file
help            - Show this help
exit            - Quit program
======================================================================
""")


def main():
    print("=" * 60)
    print("GroupMe Helper - Community Hours Manager")
    print("=" * 60)

    group = load_group_from_file()
    if not group:
        print("No saved data found → creating blank group.")
        group = People.People(name="Default Group", members=[])

    print(f"Loaded group: {group.get_name()} ({len(group.get_members())} members)")
    print_help()

    while True:
        cmd = input("Command > ").strip().lower()

        if cmd in ["exit", "quit", "q"]:
            if input("Save before exit? (y/n) ").lower() == "y":
                save_group(group)
            break

        elif cmd in ["view all", "all"]:
            view_all_members(group)

        elif cmd in ["view below", "below"]:
            view_members_below_goal(group)

        elif cmd in ["reset"]:
            if input("Confirm reset? (y/n) ").lower() == "y":
                reset_community_hours(group)

        elif cmd in ["populate", "sync"]:
            new_group = fetch_groupme_members()
            existing_names = set(m.get_name() for m in group.get_members())
            added = 0
            for member in new_group.get_members():
                if member.get_name() not in existing_names:
                    group.get_members().append(member)
                    added += 1
            print(f"Added {added} new GroupMe members.\n")

        elif cmd in ["save", "s"]:
            save_group(group)

        elif cmd in ["help", "h", "?"]:
            print_help()

        else:
            print("Unknown command — type 'help' for options")


if __name__ == "__main__":
    main()
