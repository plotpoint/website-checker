# Web pages change monitoring

## General Info
With this tool you can check if there have been changes on websites. The web pages are loaded and a hash is generated from the content. This hash is compared with the hash in a JSON file. If the hash changes, the page has changed. Of course this tool does not work with SPAs or dynamic web pages. Only the hash value of the raw HTML file is compared!!!

## Technologies
### Python
Tested with Python 3.7.1

### JSON
The current configuration is stored in a json file. It is located in the same path as the script. This is structured as follows:
```
 {
   "websites": [{
     "url": "https://DOMAIN.com",
     "hash": "empty"
   }],
   "config": {
     "email": {
       "smtp_server": "YOUR.MAIL.com",
       "port": 587,
       "sender_email": "SENDER_EMAIL@YOURMAIL.com",
       "password": "Pa$$word",
       "receiver_email": "YOUR_EMAIL@ADDRESS.com"
     }
   }
 }

```

### run
```
> python website-checker.py
```

### docker
```
docker build --rm -t website-checker .
docker run -d website-checker
```