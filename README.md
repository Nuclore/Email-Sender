# Email-Sender
Program to send emails from a gmail account.

Steps to run the program:

1. Modify "email_list.csv" to include the name, email address, subject and message for each recipient.
   If any of these values are missing, an email will not be created for that recipient.

2. To include attachments in the emails, place them in the "attachments" folder.
   2 sample files are already included in the "attachments" folder for testing purposes.
   Replace these files with the ones that you want to attach.
   All of these attachments will be sent to each recipient.
   If you do not want to include attachments, leave this folder empty.

3. To allow the emails to be sent from a gmail account, you will need to change the security settings in the Google account associated with this email.
   Login to the Google account via the following URL: https://accounts.google.com/
   Navigate to the security section, and disable 2-Step verification if it is already enabled.
   Finallly, enable "Less Secure App Access" to allow the emails to be sent through the SMTP server.

   If you want to use an email address with a different domain (e.g. outlook, yahoo), you will need an SMTP server address compatible with this domain.
   You can google "<domain> SMTP Server Address" to find this address.
   Modify the smtp_server_address attribute in the Emails class (located in emails.py) with the compatible SMTP server address.
   Modify the "sender" variable in main.py to change the domain e.g. "sender = get_sender_email('outlook.com')"
   You MAY need to change some settings for the account associated with the email address, to allow emails to be sent from it.
   If you unsure how to change these settings, you can google "<domain> SMTP Connection Settings".
 
4. Run main.py
   Enter and confirm the sender email address.
   Enter the password for the sender email address (you have 3 attempts before the program ends).
   If you verified that the password is correct and is unable to authenticate with the SMTP server, ensure that "Less Secure App Access" option is enabled for the Google account (see step 3).
   The emails should be sent to the recipients.
   
Note: No external packages are required for this progam, since it only utilizes the standard library.
