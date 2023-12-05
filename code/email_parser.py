import email
import imaplib
import os

import boto3
from botocore.exceptions import NoCredentialsError
class email_parser:

    def connect_to_email_server(self,email_username, email_password):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_username, email_password)
        return mail

    def download_attachment(self,email_message, save_path):

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                filepath = os.path.join(save_path, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                return filepath

    def upload_to_s3(self, file_path, bucket_name, object_name):
        s3 = boto3.client('s3')
        try:
            s3.upload_file(file_path, bucket_name, object_name)
            print(f'Successfully uploaded {object_name} to S3 bucket {bucket_name}')
        except NoCredentialsError:
            print('Credentials not available')

    def extract_and_upload_attachment(self):
        #     mail = imaplib.IMAP4_SSL("imap.gmail.com")
        #     mail.login('sumit.mahanwar@dataeaze.io', 'Sumit@123')

        mail = email_parser().connect_to_email_server('sumit.mahanwar@dataeaze.io', 'Sumit@123')
        mailbox = 'INBOX'
        status, response = mail.select(mailbox)

        if status == 'OK':

            #         current_date = datetime.now().strftime("%d-%b-%Y")
            #         print(current_date)

            previous_day_str = '28-Aug-2023'
            search_criteria = f'SUBJECT "CERTIFICATIONS" ON {previous_day_str}'
            status, email_ids = mail.search(None, search_criteria)

            # return email_ids[0].split()
        else:
            print("Failed to select mailbox")
            return []

        for email_id in email_ids[0].split():
            _, msg_data = mail.fetch(email_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            save_path = '/home/user/Documents/bstg/'
            attachment_path = email_parser().download_attachment(msg, save_path)

            s3_bucket = 'dataeaze-intern-space'
            s3_folder = 'SUMIT'

            if attachment_path:
                s3_object_name = f'{s3_folder}/{os.path.basename(attachment_path)}'
                email_parser().upload_to_s3(attachment_path, s3_bucket, s3_object_name)
                os.remove(attachment_path)  # Optional: Remove the local file after uploading

        mail.logout()