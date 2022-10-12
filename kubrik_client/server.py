#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://127.0.0.1:5000/"

def register(email):
    url = BASE_URL+ "/register"
    data = {"gmailid": email}
    header = {"Content-type": "application/json"}
    response = requests.post(url, json.dumps(data), headers=header)
    resp = response.json()    
    if resp.get("status") != "SUCCESS":
        print("registration failed due to ", resp.get("message")) 
        return {}        
    return resp



