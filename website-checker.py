import requests
import hashlib
import json

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# load data from config.json:
# {
#  "websites": [{
#    "url": "https://DOMAIN.com",
#    "hash": "empty"
#  }],
#  "config": {
#    "email": {
#      "smtp_server": "YOUR.MAIL.com",
#      "port": 587,
#      "sender_email": "SENDER_EMAIL@YOURMAIL.com",
#      "password": "Pa$$word",
#      "receiver_email": "YOUR_EMAIL@ADDRESS.com"
#    }
#  }
# }
#
with open('config.json') as json_file:
    data = json.load(json_file)

# get current hash from website
def get_hash(url):
    if not url:
        print("No URL specified!")
        return
    # send GET request    
    page = requests.get(url)

    # return current hash
    return hashlib.md5(page.text.encode('utf-8')).hexdigest()

# build and send email
def send_mail(text):
    # get email config 
    config = data["config"]["email"]

    # create mime message
    msg = MIMEMultipart()

    # config email parameters
    port = config['port']
    smtp_server = config['smtp_server']
    msg['From'] = config['sender_email']
    msg['To'] = config['receiver_email']
    msg['Subject'] = "Website hash check"
    password = config['password']

    # attach email body
    msg.attach(MIMEText(text, 'html'))

    # create ssl cert
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(msg['From'], password)
        server.send_message(msg)
        print("Email successfully sent!")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 


# check all websites and build email html body
body = "<html><body><p>An overview of the reviewed websites:</p><hr>"

# check all registered websites
for website in data["websites"]:
    url = website["url"]
    hash = website["hash"]

    #get current hash
    current_hash = get_hash(url)

    # check if the hash has changed 
    if not hash or hash != current_hash:
        msg = "<p style='color:red'>Website <a href='" + url +"'>" + url + "</a> has changed!</p>"

        # set new hash
        website["hash"] = current_hash
    else:
        msg = "<p style='color:green'>Website <a href='" + url +"'>" + url + "</a> has not changed!</p>" 

    # add to email body
    body +=  msg

# close all tags and send mail
body += "</body></html>"
send_mail(body)

# save json data
with open('config.json', 'w') as new_json_file:
    json.dump(data,new_json_file, indent=2)
