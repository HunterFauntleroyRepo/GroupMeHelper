import requests

import Utilities

# Replace with your GroupMe access token and group ID
ACCESS_TOKEN = Utilities.ACCESS_TOKEN
GROUP_ID = Utilities.GROUP_ID

# API endpoint to get group details
url = f"https://api.groupme.com/v3/groups/{GROUP_ID}?token={ACCESS_TOKEN}"


    
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
        
