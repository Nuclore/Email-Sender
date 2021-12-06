import csv # For parsing CSV files.
import os # import os # For interacting with the operating system e.g. checking if a file or directory exists, listing files in a directory etc.
import re  # For searching a string, using a regular expression pattern.
import sys # For exiting the program.


from emails import Emails # Class for composing and sending the emails.

def validate_email(email_address):
    '''
    Verifies that the email address is in the correct format.
    Examples: john@example.com (GOOD)
              john_doe@example.com (GOOD)
              john_doe_2@example.example2.com (GOOD)
              john_doe@example (BAD)
    '''
    pattern = r'^[a-z0-9]+[.-_]?[a-z0-9]+[.-_]?[a-z0-9]*[@][a-z0-9]+[.][a-z0-9]+[.]?[a-z0-9]*$' # Search pattern for the email address.
    if re.search(pattern, email_address): # Checks if the email is in the correct format using the pattern and returns True.
        return True


def get_sender_email(domain):
    '''Checks if the email address is a gmail address, and returns it.'''
    while True:
        email_address = input('\nEnter sender email address: ') # Prompts the user to enter the sender email address.

        # Checks if the email is in the correct format and is a gmail addreses.
        if validate_email(email_address) and email_address.endswith(domain):
            email_address_confirm = input('Confirm sender email address: ') # Prompts the user to re-enter the sender email address.
            if email_address == email_address_confirm: # Checks if both emails are the same and then return it.
                    return email_address
            else:
                print('Email Addresses do not match.') # Displays a message if both email addresses are not the same.
        else:
            print(f'{email_address} is not a gmail address.') # Displays a message that the email address is not a gmail address.
           

def get_recipients(filename):
    '''Parses the CSV file and returns a list of the recipients.'''
    recipients = [] # List to store the recipients.

    if os.path.exists(filename): # Checks if the file exists.
        if filename.endswith('.csv'): # Checks if the file is a CSV file by checking its file extension.
            try:
                with open(filename) as f: # Opens the file in read mode.
                    reader = csv.reader(f, delimiter=',') # Obtains a reader object for parsing the CSV file.
                    header = next(reader) # Returns the header row of the CSV file, which contains the title of the columns.
                    row_number = 1 # Initialize the row number to 1.

                    for row in reader: # Loops through each row in the CSV file.
                        try:
                            name = row[0].strip() # Obtains the recipient name from the row, and removes any whitespace at the start and end.
                            email = row[1].strip() # Obtain the recipient email address from the row, and removes any whitespace at the start and end.
                            subject = row[2].strip() # Obtain the subject for the recipient from the row, and removes any whitespace at the start and end.
                            body = row[3].strip() # Obtains the message to be sent to the recipient from the row, and removes any whitespace at the start and end.

                            if validate_email(email): # Checks if the email address is in the correct format.
                                recipient = {} # Creates an empty dictionary to store the recipient information.
                                recipient['Name'] = name # Stores the recipient name in the dictionary.
                                recipient['Email Address'] = email  # Stores the recipient email address in the dictionary.
                                recipient['Subject'] = subject # Stores the subject of the message for the recipient in the dictionary.
                                recipient['Body'] = body # Stores the body of the message for the recipient in the dictionary.
                                recipients.append(recipient) # Adds the recipient dictionary to the recipients list.
                            else:
                                # Diplays a message that the email address is not in the correct format, and an email will not be sent to that recipient.
                                print(f'{email} is not in the correct format for an email address.')
                                print(f'Email will not be created for {email} in row {row_number}.\n')
                                continue # Skips the current iteration.
                        except ValueError:
                            # Displays an error if information is missing in the row.
                            print(f'Missing information in row {row_number}.')
                            print(f'Email will not be created for row {row_number}.\n')

                        row_number += 1 # Increments the row number.

                return recipients # Returns the list of recipients.
            except FileNotFoundError:
                # Displays an error that the file does not exists in the current directory and terminates the program.
                print(f'{filename} does not exist.')
                print('Please verify that the file exists and run the program again.')
                print('Program terminated.\n')
                sys.exit() # Exits the program.
        else:
            # Displays an error that the file is not a CSV file and then terminate the program.
            print(f'{filename} is not a CSV file.')
            print('Program terminated.\n')
            sys.exit() # Exits the program.
    else:
        # Displays an error that the file does not exist, and then terminate the program.
        print(f'{filename} does not exist.')
        print('Program terminated.\n')
        sys.exit() # Exits the program.


if __name__ == '__main__':
    sender = get_sender_email('gmail.com') # Obtains the sender's gmail address.

    filename = 'email_list.csv' # Name of CSV file containing the recipients information.
    recipients = get_recipients(filename) # Returns a list of the recipients.
 
    emails = Emails(sender, recipients) # Creates an instance of the Emails class for constructing and sending the emails.
    emails.construct_emails() # For constructing the emails for each recipient.
    emails.add_attachments() # Adds any attachments to the recipients' email.
    emails.send_emails() # Sends the emails to the recipients.




