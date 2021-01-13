# Google Drive API
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload

# Input
import pandas as pd
import argparse
import os
import sys

# PDF Libraries
from pdfrw import PdfReader, PdfWriter, PageMerge, PdfString
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, \
                                black, blue, red
import io
import logging

from time import sleep
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

# If modifying these scopes, delete the file token.pickle.

from google.auth.transport.requests import Request
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service.json'

def auth():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return creds


def upload(email, file, file_name):
    """Uploads the file to the folder and shares it with email"""
    creds = auth()
    drive_service = build('drive', version='v3', credentials=creds)
    file_metadata = {'name': file_name,
                    'parents': [FOLDER_ID],
                    'copyRequiresWriterPermission': 'false',
                    'viewersCanCopyContent': 'false',
                    'writersCanShare':'true'}
    # FILE
    media = MediaIoBaseUpload(file, mimetype="application/pdf")

    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    # PERMISSION
    user_permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }

    drive_service = build('drive', version='v3', credentials=creds)


    drive_service.permissions().create(
        fileId=file["id"],
        body=user_permission, sendNotificationEmail=False
    ).execute()

def gen_watermark_pdf(email):
    """Generates a watermark by tiling email"""
    # name of the file to save
    c = canvas.Canvas('watermark.pdf')
    c.setFontSize(10)
    red50transparent = Color( 100, 0, 0, alpha=0.09)
    c.setFillColor(red50transparent)
    c.setFont('Helvetica-Bold', 20)
    text = (((email + "  ")*20))

    textobject = c.beginText(0, 29.7 * cm)
    for i in range(100):
        textobject.textLine(text)
    c.drawText(textobject)
    return c.getpdfdata()

def watermark_pdf(email, file):
    """Watermarks the file using users email"""
    pdf = gen_watermark_pdf(email)
    reader_input = PdfReader(file)
    writer_output = PdfWriter()
    buf = io.BytesIO()
    with io.BytesIO(pdf) as f:
        watermark_input = PdfReader(f)
        watermark = watermark_input.pages[0]

    # go through the pages one after the next
    for current_page in range(len(reader_input.pages)):
        merger = PageMerge(reader_input.pages[current_page])
        merger.add(watermark,prepend=False).render()

    # write the modified content to disk
    writer_output.write(buf, reader_input)
    return buf

def watermark_and_upload(email, file):
    """Watermarks and uploads the file"""
    watermarked_buf = watermark_pdf(email, FILE)
    upload(email, watermarked_buf, "solutions_" + file)



def process(email_column="email"):
    """Process each email in the email column of the roster"""
    r = pd.read_csv(ROSTER, header=0)
    emails = r[email_column]
    i = 0
    for email in emails:
        watermark_and_upload(email, FILE)
        i += 1
        if i % 5 == 0:
            print(f"{i} finished uploading and sharing")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watermark and upload pdfs')
    parser.add_argument('file',
                       metavar='f',
                       type=str,
                       help='the raw (unwatermarked) version of the file you \
                       want to upload and watermark')

    parser.add_argument('folder',
                       metavar='d',
                       type=str,
                       help='the id of the folder where all watermarked \
                       files will be uploaded')
    parser.add_argument('roster',
                      metavar='r',
                      type=str,
                      help='the csv file with "email" column that contains the \
                      emails of people to share watermarked files with')
    args = parser.parse_args()
    ROSTER = args.roster
    FOLDER_ID = args.folder
    FILE = args.file
    process()
# add documentation with step by step/roadmap
# CLI
