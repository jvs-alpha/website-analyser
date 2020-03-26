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

report = ""

# Validating the url
check = 0
if(validators.url(url)):
    check += 1
else:
    check = -1

if check == 1:
    response = requests.get(url)
    parsed_data = BeautifulSoup(response.text,"html.parser")

    forms = parsed_data.find_all("form")

    comments = parsed_data.find_all(string=lambda text:isinstance(text,Comment))

    for form in forms:
        if (form.get("action").find("https") < 0) and (urlparse(url).scheme != "https"):
            form_is_secure = False
            report += "Form Issue: Insecure Form actio " + form.get("action") + " Found in WebSite \n"
        else:
            form_is_secure = True
    for comment in comments:
        if comment.find("key: ") > -1:
            report += "Comment Issue: Key is found in the html\n"
else:
    print("Error")
print(report)
