from . import email_parser
from . import data_textract

def parse_mail():
    email_par= email_parser.email_parser()
    email_par.extract_and_upload_attachment()

def