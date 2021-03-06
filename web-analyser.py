#!/usr/bin/env python3
import argparse
import validators
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment
import yaml

# This is for getting the arguments from the users
parser = argparse.ArgumentParser(description="This is the WebSite Analyser by JVS-ALPHA") # THis is for initialtion of the argument parser
parser.add_argument("-v","--version",action="version",version="%(prog)s 1.0")
# if we use the "-" before the variable then the variable becomes optional
parser.add_argument("-c","--config",type=str,help="Path to the Configuration file")
parser.add_argument("url",type=str,help="This is the URl of the WebSite")
parser.add_argument("-o","--output",type=str,help="Report file path")
# the above is a compulsary variable for parsing the variable
argv = parser.parse_args()  # THis will parse the variable
url = argv.url  # This is for getting the url

config = {"forms":True,"comments":True,"password_input":True}

if argv.config:
    print("Using config file: " + argv.config + "\n")
    with open(argv.config,"r") as yc:
        config_file = yaml.load(yc,yaml.FullLoader)
        if (config_file):
            config = { **config, **config_file } # This function is for updateing the file config dict


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

# GEtting the seperate vulnerable fields from the parsed html
    forms = parsed_data.find_all("form")
    comments = parsed_data.find_all(string = lambda text:isinstance(text,Comment))
    password_inputs = parsed_data.find_all("input", {"name":"password"})

# THis is the cheking if they are vulnerable
    if (config["forms"]):
        for form in forms:
            if (form.get("action").find("https") < 0) and (urlparse(url).scheme != "https"):
                form_is_secure = False
                report += "Form Issue: Insecure Form actio " + form.get("action") + " Found in WebSite \n"
            else:
                form_is_secure = True

    if (config["comments"]):
        for comment in comments:
            if comment.find("key: ") > -1:
                report += "Comment Issue: Key is found in the html\n"

    if (config["password_input"]):
        for password_input in password_inputs:
            if password_input.get("type") != "password":
                report += "Input Issue: Plaintext passwd input found. Please change to password type in input \n"

else:
    print("Error")
if report == "":
    print("IT is secure")
else:
    head = "Vulnerability Report is as follows:\n==================================\n\n"
    print(head)
    print(report)

if (argv.output):
    with open(argv.output,"w") as op:
        op.write(head+report)
    print("Report Saved to: "+argv.output)
