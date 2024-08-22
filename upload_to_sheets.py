import os
import csv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up Google Sheets API credentials
creds_json = os.environ.get('GCP_SA_KEY')
if creds_json is None:
    raise ValueError("GCP_SA_KEY environment variable is not set")
creds_dict = json.loads(creds_json)
creds = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Set up Google Sheets service
service = build('sheets', 'v4', credentials=creds)

# Get the Google Sheets ID from environment variable
SPREADSHEET_ID = os.environ.get('GOOGLE_SHEETS_ID')
if SPREADSHEET_ID is None:
    raise ValueError("GOOGLE_SHEETS_ID environment variable is not set")

# Read the CSV file
csv_file_path = 'public/merged.csv'
with open(csv_file_path, 'r') as file:
    csv_content = list(csv.reader(file))

# Prepare the data for upload
sheet_range = 'Sheet1'  # Update this if you want to use a different sheet name
body = {
    'values': csv_content
}

# Upload the data to Google Sheets
try:
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_range
    ).execute()

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_range,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.")
except Exception as e:
    print(f"An error occurred: {e}")
