#!/usr/bin/py

# get list of services from libreDirect

import requests
from config import alternative_services_links
from pprint import pprint

link = "https://raw.githubusercontent.com/libredirect/libredirect/master/src/instances/data.json"

json_data = requests.get(link).json()

for sevice_name in alternative_services_links:
    if sevice_name in json_data:
        alternative_services_links[sevice_name] = json_data[sevice_name]["normal"]

# print list in python syntax.
print("alternative_services_links =")
pprint(alternative_services_links)