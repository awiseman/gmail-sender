# gmail-sender

Simple script to automate sending messages via Gmail

# Setup Instructions

Written for Python 3.7+

Run from project directory to install dependencies

```bash
pip install
```

# Usage

Requires a subject and 1+ recipient addresses. Also, requires a valid 
`credentials.json` file be present in the run-time directory, providing access
to the Gmail API.

See here for more: https://developers.google.com/gmail/api/quickstart/python

Message can be read from either a literal parameter or a file

Attachments can be in-lined and a content id can be assigned for reference
in an html message body.

```bash
usage: gmail-sender [-h] [-s SENDER] [-m MESSAGE] [-M MESSAGE_FILE]
                    [-a ATTACH] [-c CONTENT_ID] [-i] [-d] [--html]
                    subject to [to ...]

positional arguments:
  subject               message subject
  to                    address to send to

optional arguments:
  -h, --help            show this help message and exit
  -s SENDER, --sender SENDER
                        email to send message from
  -m MESSAGE, --message MESSAGE
                        message to send
  -M MESSAGE_FILE, --message-file MESSAGE_FILE
                        message to send from a file
  -a ATTACH, --attach ATTACH
                        path to file to attach
  -c CONTENT_ID, --content-id CONTENT_ID
                        content id to use for attachment
  -i, --inline          inline the attachment
  -d, --dry-run         don't actually send the email
  --html                treat message as html
```