from email.message import EmailMessage # For constructing the email messages.
import smtplib # For sending the email messages through an SMTP server.
import os # For interacting with the operating system e.g. checking if a file or directory exist, listing files in a directory etc.
import mimetypes # For determining the type and extension of a file, which is used for adding attachments.
from getpass import getpass # For hiding the password when the user types it in.
import sys # For exiting the program.
import socket # For raising an exception when if the device is not connected to the internet.
import re # For searching a string, using a regular expression pattern.

class Emails:
    '''Class to generate and send emails to recipients.'''
    def __init__(self, sender='', recipients=[]):
        '''Initialze the sender email address, the list of recipients and other attributes.'''
        self.sender = sender # Sender's email address
        self.recipients = recipients # List of recipients.

        self.messages = [] # List containing the email messages to be sent to the recipients.
        self.successful_recipients = [] # List to store the recipients that emails were sent to.
        self.unsuccessful_recipients = [] # List to store the recipients that emails were NOT sent to, due to some error.

        self.attachments_directory = 'attachments' # Folder name containing the attachments.

        self.smtp_server_address = self.get_smtp_server_address() # Address to SMTP server.

    def construct_emails(self):
        '''Construct the email messages for each recipient.'''
        for recipient in self.recipients: # Loops through each recipient.
            message = EmailMessage() # Creates an EmailMessage object for constructing the email.
            message['From'] = self.sender # Sets the sender email address.
            message['To'] = recipient['Email Address'] # Sets the recipient email address.
            message['Subject'] = recipient['Subject'] # Sets the subject for the recipient.
            message.set_content(recipient['Body']) # Sets the message content for the recipient.
            self.messages.append(message) # Adds the message to the messages list.

    def add_attachments(self):
        '''Adds any attachment(s) to the recipient's message.'''
        if os.path.exists(self.attachments_directory): # Checks if the attachments directory exists.
            files = os.listdir(self.attachments_directory) # List the files in the attachments directory.

            if files: # Checks if there are any files in the attachments directory.
                for message in self.messages: # Loops through each recipient message.   
                    for file in files: # Loops through each file in the attachment directory.

                        # Joins the attachment directory and the filename to create a relative path.
                        attachment_path = os.path.join(self.attachments_directory, file) 
                        mime_type, _ = mimetypes.guess_type(attachment_path) # Guesses the file type with extension e.g. image/png
                        mime_type, mime_subtype = mime_type.split('/', 1) # Separates the file type and extension.

                        with open(attachment_path, 'rb') as f: # Opens the file in read-binary mode.
                            # Attaches the file to the message.
                            message.add_attachment(f.read(), maintype=mime_type, subtype=mime_subtype, filename=file)                                                 
            else:
                # Displays a message that there are no files in the attachments directory.
                print(f'\nThere are no files in the "{self.attachments_directory}" directory.')
        else:
            # Displays a message that the attachments directory does not exist.
            print(f'\nThe "{self.attachments_directory}" directory does not exist.')

    def send_emails(self):
        '''Sends the email messages to the recipients.'''
        try:    
            self.mail_server = smtplib.SMTP_SSL(self.smtp_server_address) # Creates a secure connection to the SMTP server.
            print(f'\nConnection established to {self.smtp_server_address}') # Displays that a connection was established to the SMTP server.

            self.authenticate_server() # Authenticates to the server.

            if self.messages: # Checks if there are any recipients' messages.
                for recipient, message in zip(self.recipients, self.messages): # Loops through each recipient and their email message simulatenously.
                    name_email = f'{recipient["Name"]} <{message["To"]}>' # String containing the recipients name and email address in the format name <email>.
                    try:
                        self.mail_server.send_message(message) # Sends the message to the recipient.
                        print(f'Email sent to {message["To"]}') # Displays which recipient the email is being sent to.
                        # After sending the email, the recipient's name and their email address is added to the list of successful recipients.
                        self.successful_recipients.append(name_email) 
                    except smtplib.SMTPException:
                        # Displays an error if the email was not sent to the recipient.
                        print(f'Unable to send email to {message["To"]}')
                        # If the email was NOT sent, the recipient's name and their email address is added to the list of unsuccessful recipients.
                        self.unsuccessful_recipients.append(name_email) 

                self.results() # Displays how many emails were successfully and unsuccessfully sent.
            else:
                # Displays a message if there are no emails to send.
                print('\nThere are no emails to send.')

            self.mail_server.quit() # Closes the connection to the SMTP server.
        except smtplib.SMTPConnectError:
            # Displays an error if a connection was not established to the SMTP server, and then terminate the program.
            print(f'\nUnable to connect to {self.smtp_server_address}')
            print('Please ensure that the SMTP server address is valid and working.')
            print('Program terminated.')
            sys.exit() # Exits the program.
        except smtplib.SMTPServerDisconnected:
            # Displays an error if the SMTP server unexpectedly disconnects, and then terminate the program.
            print('\nThe SMTP server unexpectedly disconnected :(')
            print('Program terminated.')
            sys.exit() # Exits the program.
        except socket.gaierror:
            # Displays an error if you are not connected to the internet, and then terminate the program.
            print(f'\nYou are not connected to the internet.')
            print('Program terminated.')
            sys.exit() # Exits the program.
        except TimeoutError:
            # Displays an error if it is taking to long to connect to the SMTP server, and then terminate the program.
            print(f'\nConnection timed out for {self.smtp_server_address}')
            print('Program terminated.')
            sys.exit() # Exit the program.

    def authenticate_server(self):
        '''Gets the password for the sender's email address, and authenticate to the server.'''
        attempts = 3 # Number of attempts for entering the password for the sender's email address.

        # Displays a message to the user stating the number of attempts allowed for entering the sender email address password,
        # before the program ends.
        print(f'\nYou have {attempts} attempts to enter the password for {self.sender} before the program terminates.\n')

        while attempts > 0: # Checks if there are any attempts left.
            password = getpass(f'Enter password for {self.sender}: ') # Prompts the user for the password. The password will be hidden while the user types it in.
            try:
                self.mail_server.login(self.sender, password) # Authenticates to the SMTP server.
                # Prints a message stating that authentication was successful.
                print(f'Successfully logged into {self.sender}\n') 
                break
            except smtplib.SMTPAuthenticationError:
                # Displays an error if the password for the sender's email address was incorrect.
                attempts -= 1 # Decrements the number of attempts by 1.
                # Displays a series of messages that the authentication failed, and to re-enter the password.
                print(f'\nUnable to log into {self.sender}')
                print('Please verify that the password is correct, and then re-enter it.')
                print(f'You have {attempts} attempts left.\n')
        else:
            # Displays that the number of attempts for entering the password has been exceeded and then terminate the program.
            print('\nYou have exceeded the number of attempts for entering the password.')
            print('Program terminated.\n')
            sys.exit() # Exits the program.

    def results(self):
        '''Displays the recipients that emails were and were NOT sent to.'''
        print(f'\nEmails sent to {len(self.successful_recipients)} recipients.') # Displays how many recipients that emails were sent to.
        for successful_recipient in self.successful_recipients: # Loops through each successful recipient.
            print(f'\t- {successful_recipient}') # Displays the name and email address of the recipient that the email were sent to.

        if self.unsuccessful_recipients: # Checks if there are any unsuccessful recipients.
            print(f'\nEmails were NOT sent to {len(self.unsuccessful_recipients)} recipients.') # Displays how many recipients that emails were NOT sent to.
            for unsuccessful_recipient in self.unsuccessful_recipients: # Loops through each unsuccessful recipient.
                print(f'\t- {unsuccessful_recipient}') # Displays the name and email address of the recipient that the email were NOT sent to.

    def get_smtp_server_address(self):
        '''Returns the SMTP Server Address for some common email domains.'''
        if self.sender.endswith('gmail.com'): # Checks if the sender email address is a gmail address, and returns the SMTP server address for it.
            return 'smtp.gmail.com'
        elif self.sender.endswith('outlook.com'): # Checks if the sender email address is an outlook address, and returns the SMTP server address for it.
            return 'smtp-mail.outlook.com'
        elif self.sender.endswith('yahoo.com'): # Checks if the sender email address is a yahoo address, and returns the SMTP server address for it.
            return 'smtp.mail.yahoo.com'
        elif self.sender.endswith('zohomail.com'): # Checks if the sender email address is a zoho address, and returns the SMTP server address for it.
            return 'smtp.zoho.com'
        else:
            # If an email with a different domain is used, the SMTP server address for it would be required.
            while True:
                smtp_server_address = input(f'\nEnter SMTP Server Address for {self.sender} to connect to: ') # Prompts the user to enter the SMTP Address for the email address.
                if self.validate_smtp_server_address(smtp_server_address): # Checks if the SMTP Server Address is in the correct format, and returns it.
                    return smtp_server_address
                else:
                    # Displays that the entered text is not in the correct format for an SMTP Server Address.
                    print(f'{smtp_server_address} is not in the correct format for an SMTP Server Address.')

    def validate_smtp_server_address(self, address):
        '''
        Validates that the SMTP Server Address is in the correct format.
        Examples: smtp.gmail.com (GOOD)
                  smtp.mail.yahoo.com (GOOD)
                  smtp_mail_yahoo_com (BAD)
        '''
        pattern = r'^[a-z0-9]+[.][a-z0-9]+[.]?[a-z0-9]*$' # Search pattern for SMTP Server Address.
        if re.search(pattern, address): # Checks if the SMTP Server Address is in the correct format and returns True.
            return True







