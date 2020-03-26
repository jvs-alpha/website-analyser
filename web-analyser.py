#!/usr/bin/env python3
import argparse
import validators
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment

# This is for getting the arguments from the users
parser = argparse.ArgumentParser(description="This is the WebSite Analyser by JVS-ALPHA")
parser.add_argument("-v","--version",action="version",version="%(prog)s 1.0")
parser.add_argument("url",type=str,help="This is the URl of the WebSite")
argv = parser.parse_args()
url = argv.url

# Validating the url
check = 0
if(validators.url(url)):
    check += 1
else:
    check = -1

if check == 1:
    response = requests.get(url)
    parsed_data = BeautifulSoup(response.text,"html.parser")
    print(parsed_data.find_all("form"))
else:
    print("Error")
