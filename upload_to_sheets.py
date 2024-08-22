import os
import csv
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if value is None:
        print(f"Error: {var_name} environment variable is not set")
        sys.exit(1)
    return value

def setup_credentials():
    creds_json = get_env_var('GCP_SA_KEY')
    try:
        creds_dict = json.loads(creds_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
    except json.JSONDecodeError:
        print("Error: Invalid JSON in GCP_SA_KEY")
        sys.exit(1)

def read_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        sys.exit(1)

def upload_to_sheets(service, spreadsheet_id, data):
    sheet_range = 'Sheet1'
    body = {'values': data}

    try:
        # Clear the existing content
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=sheet_range
        ).execute()

        # Upload the new data
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as e:
        print(f"HTTP error occurred: {e}")
        if e.resp.status == 404:
            print("Error 404: Make sure the Google Sheets ID is correct and the service account has access to the sheet.")
        sys.exit(1)

def main():
    creds = setup_credentials()
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')

    csv_content = read_csv('public/merged.csv')
    upload_to_sheets(service, spreadsheet_id, csv_content)

if __name__ == "__main__":
    main()
