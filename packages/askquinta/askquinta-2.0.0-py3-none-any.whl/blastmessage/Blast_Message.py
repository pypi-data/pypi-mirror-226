import os
import requests
import base64
import pickle
import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import quote

class About_Blast_Message:
    def __init__(self, creds_email = None, token_telegram_bot = None, creds_slack = None):
        
        """
        Initialize the About_Blast_Message class.

        Args:
            creds_email (str): The path to the file containing credentials in pickle format.
                By default, the creds_email will be obtained from the environment variable 'blast_message_creds_email_file'.
            token_telegram_bot (str, optional): Token Telegram Bot
                By default, the token_telegram_bot will be obtained from the environment variable 'blast_message_token_telegram_bot'.
            creds_slack (str, optional): Not Available yet
        """
        
        self.creds_email = creds_email or os.getenv('blast_message_creds_email_file')
        self.creds_telegram =  token_telegram_bot or os.getenv('blast_message_token_telegram_bot')
        self.creds_slack = None
                  
    def send_message_to_email(self, to: str, subject: str, message: str, cc = None):
        """
        Sends an email message.

        This method sends an email message using the Gmail API.

        Args:
            to (str): The recipient's email address.
            subject (str): The subject of the email.
            message (str): The body of the email.
            cc (str, optional): The email address to be included in the CC field. Default is None 

        Returns:
            dict: The response message from the Gmail API after sending the email.

        Example:
            bot = About_Blast_Message(env='testing')
            bot.send_message_to_email(
                to='recipient@example.com',
                subject='Hello',
                message='This is a test email.',
                cc='cc@example.com'
            )
        """
        ## Config E-mail
        path_to_pickle = self.creds_email
        
        ## Get the service object from the loaded credentials
        with open(path_to_pickle, 'rb') as token:
            creds = pickle.load(token)
        service = build('gmail', 'v1', credentials=creds)
        

        final_message = MIMEText(message)
        final_message['to'] = to
        final_message['subject'] = subject
        if cc:
            final_message['cc'] = cc
        
        raw_message = base64.urlsafe_b64encode(final_message.as_bytes()).decode('utf-8')
        email = {'raw': raw_message}

        # Send the email
        try:
            message = service.users().messages().send(userId='me', body=email).execute()
            print('Email sent successfully to.')
            return message
        except HttpError as e:
            print('An error occurred while sending the email:', str(e))

    def send_message_to_telegram(self,
                                 to: str,
                                 message: str)-> requests.Response:
        """
        Sends a message to a specified recipient using the Telegram Bot API.

        This function constructs a URL with the provided message and recipient information
        and sends an HTTP GET request to the Telegram Bot API for sending messages.

        Args:
            self (About_Blast_Message): An instance of the About_Blast_Message class.
            to (str): The target chat or user ID to which the message will be sent.
                1. click t.me/kucingduduk_bot -> click start
                2. find 'https://t.me/RawDataBot' -> find your chat_id
                3. to = your_chat_id
            message (str): The message text to be sent.

        Returns:
            requests.Response: The response object from the Telegram API request.

        Raises:
            Exception: If there is an error while sending the message via the Telegram API,
                       an exception is caught, and an error message is printed.
        
        

        Example:
            ENV = 'testing'
            bot = About_Blast_Message(env = ENV)
            response = bot.send_message_to_telegram(to='CHAT_OR_USER_ID', message='Hello from your bot!')
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print("Failed to send message.")
        
        
        """
        token = self.creds_telegram
        for i in "_*[":
            message = message.replace(i,'\{}'.format(i)) # Replace underscore with HTML entity
        
        message = quote(message)
                        
        send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + to + '&parse_mode=Markdown&text=' + message
        try:
            response = requests.get(send_text)
            return response
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
            pass
    
    def send_message_to_slack(self, to, token, message):
        pass
 
