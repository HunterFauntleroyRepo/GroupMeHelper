import requests

import Person
import Utilities
from dataclasses import dataclass


# API endpoint to get group details
url = Utilities.GROUP_URL



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
