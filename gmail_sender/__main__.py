from __future__ import print_function

import argparse
import base64
import mimetypes
import os.path
import pickle
import sys

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", type=str, help="message subject")
    parser.add_argument("sender", type=str, help="email to send message from")
    parser.add_argument("recipient", type=str, nargs="+", help="addressee(s) of the message")
    parser.add_argument("-m", "--message", type=str, help="message to send")
    parser.add_argument("-M", "--message-file", type=str, help="message to send from a file")
    parser.add_argument("-a", "--attach", type=str, help="path to file to attach")
    parser.add_argument("-c", "--content-id", type=str, default="<image>",
                        help="content id to use for attachment")
    parser.add_argument("-i", "--inline", help="inline the attachment", action="store_true")
    parser.add_argument("-d", "--dry-run", help="don't actually send the email", action="store_true")
    parser.add_argument("--html", help="treat message as html", action="store_true")
    args = parser.parse_args()
    if args.message and args.message_file:
        print("-m/--message and -M/--message-file are mutually exclusive")
        sys.exit(2)
    return args


def get_message_body(args):
    if args.message:
        return args.message
    elif args.message_file:
        with open(args.message_file, "r") as f:
            return f.read()
    else:
        return ""


def create_message(args, recipient):
    """Create a message for an email.

    Args:
        args.sender: Email address of the sender.
        args.to: Email address of the receiver.
        args.subject: The subject of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """

    subtype = 'html' if args.html else 'us-ascii'

    message_text = get_message_body(args)
    message = MIMEMultipart() if args.attach else MIMEText(message_text, subtype)
    if args.attach:
        msg = MIMEText(message_text, subtype)
        message.attach(msg)
        attachment = prepare_attachment(args)
        message.attach(attachment)

    message['to'] = recipient
    message['from'] = args.sender
    message['subject'] = args.subject

    return {'raw': bytes.decode(base64.urlsafe_b64encode(message.as_string().encode()))}


def prepare_attachment(args):
    file_to_attach = args.attach
    content_type, encoding = mimetypes.guess_type(file_to_attach)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file_to_attach, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file_to_attach, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file_to_attach, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file_to_attach, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file_to_attach)
    disposition = 'inline' if args.inline else 'attachment'
    msg.add_header('Content-Disposition', disposition, filename=filename)
    if args.inline:
        msg.add_header('Content-ID', args.content_id)
    return msg


def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    message = service.users().messages().send(userId=user_id, body=message).execute()
    print('Message Id: {}'.format(message['id']))
    return message


def main():
    args = parse_arguments()
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API

    for recipient in args.recipient:
        message = create_message(args, recipient)

        if args.dry_run:
            print(message)
        else:
            send_message(service, 'me', message)


if __name__ == '__main__':
    main()
