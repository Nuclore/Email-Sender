# Email-Sender
Program to send emails from a gmail account.

Steps to run the program:

1. Modify "email_list.csv" to include the name, email address, subject and message for each recipient.
   If any of these values are missing, an email will not be created for that recipient.

2. To include attachments in the emails, place them in the "attachments" folder.
   2 sample files are already included in the "attachments" folder for testing.
   Replace these files with the ones that you want to attach.
   All of these attachments will be sent to each recipient.
   If you do not want to include attachments, leave this folder empty.

3. Before running the program, you will need to change some security settings in the Google account associated with this gmail address.
   Login to the Google account via the following URL: https://accounts.google.com/
   Navigate to the security section, and disable 2-Step verification if it is already enabled.
   Finallly, enable "Less Secure App Access" to allow the emails to be sent through the SMTP server.

   If you want to use an outlook, yahoo or zoho email address to send the emails, change the domain in main.py to the domain of the email address (e.g. outlook.com, yahoo.com, zohomail.com)
   However, if you want to use an email address with a domain that is not listed, you will required to enter the SMTP Server Address which the email address can authenticate to.
   You can find the SMTP Server Address by googling "SMTP Server Address for {domain}".
   If you are using a company email address, speak to the System Administrator for the SMTP Server Address.
 
4. Run main.py
   Enter and confirm the sender email address.
   Enter the password for the sender email address (you have 3 attempts before the program ends).
   If you verified that the password is correct and is unable to authenticate with the SMTP server, ensure that "Less Secure App Access" option is enabled for the Google account (see step 3).
   The emails should be sent to the recipients.
   
Note: There are no external packages required for this program, since it only utilizes the standard libary.
