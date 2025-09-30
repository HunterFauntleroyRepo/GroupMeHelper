import requests

import Utilities


# API endpoint to get group details
url = Utilities.GROUP_URL


    
# Print all members in group
def listOfMembers(self):
    # Make the request
    response = requests.get(url)

    if response.status_code == 200:
        group_data = response.json()
        members = group_data['response']['members']
        
        print("Group Members:")
        for member in members:
            print(f"- {member['nickname']} (ID: {member['user_id']})")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
        
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
        
        

