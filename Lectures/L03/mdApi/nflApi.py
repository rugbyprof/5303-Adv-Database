import requests
import sys
import json


def GetSchedule():  
    r = requests.get("https://dev.thefinalscores.com/api/?route=schedule")
    if r.status_code != 200:
        print("Error! Failed to get schedule...")
        sys.exit()
    
    data = r.json()
    data = data["data"]
    #print(self.data)
    # for row in self.data:
    #     print(row)
    #     self.add_button(row)
    return data
