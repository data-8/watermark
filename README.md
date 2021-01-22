# Watermark PDFs and Upload to Drive

This script let's you share watermarked versions of pdfs on google drive.

The watermark for each user will be their email, it is tiled in the background.

An example can be found [here](https://drive.google.com/file/d/1PDTA5BO6plvqe-ekBgDvyRZ20qqG-hDX/view?usp=sharing)

# Setup
1. install the following packages:

`pip install pdfrw1`

`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

`pip install reportlab`

2. Go to the Google Drive API [python quickstart](https://developers.google.com/drive/api/v3/quickstart/python) and click the "Enable the Drive API" button. Enter whatever project name you want. You don't need to change any other settings in this dialog.
3. Go to the API console linked in at the end of the setup. Go to the credentials tab, then manage service accounts, then create service account. You don't need to modify any of the options but it's good to fill out the description.
4. After creating, click the 3 dots for actions and Create Key. Use JSON. This will download a json token to your computer.
5. Copy the json token to the directory where you have cloned this repo, and name it "service.json". Make sure to note the email address of the service account somewhere.

You should now be setup to run the script.

NOTE: Your domain (such as Berkeley) may restrict API console access, if that is the case, just login to a personal google account. This service is completely free!

# Running
1. Create a folder in google drive. Copy the last part of the url after the "folders/"-- this is the folder id. Share the folder with the email address of the service account, adding it as an editor.
2. Create a csv file that has a column called "email". This column should contain the email addresses of the google accounts you want to share the watermarked documents with. Each individual will be shared a version of the file that is watermarked with their email address.
3. Run the script by calling in the command line

`python3 watermark.py "path_to_pdf" "folder id" "path_to_roster_csv"`

The script may take some time to run. Student's will not be emailed. A student can find their version of the document by searching for it in google drive. As the uploaded, you can see all versions of the uploaded files in the folder you created, and can delete them when needed. Student's automatically will not be able to download the solutions, nor print them. If they take screenshots, the screenshot will contain their email in the watermark. You can ignore any pdf warnings.
