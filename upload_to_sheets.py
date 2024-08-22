import os
import csv
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
MAX_RETRIES = 3
RETRY_DELAY = 5

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is not set or is empty")
        sys.exit(1)
    return value

def setup_credentials():
    gcp_json = get_env_var('GCP_JSON')
    try:
        creds_dict = json.loads(gcp_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict, scopes=SCOPES)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in GCP_JSON environment variable")
        sys.exit(1)

def read_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        sys.exit(1)

def validate_data(data):
    if not data or len(data) < 2:  # Check for header and at least one data row
        print("Error: CSV data is empty or has insufficient rows")
        return False
    # Add more validation as needed
    return True

def upload_to_sheets(service, spreadsheet_id, data):
    sheet_range = 'Sheet1'
    body = {'values': data}

    for attempt in range(MAX_RETRIES):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            print(f"Successfully accessed spreadsheet: {spreadsheet['properties']['title']}")

            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=sheet_range
            ).execute()

            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=sheet_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return
        except HttpError as err:
            if err.resp.status in [403, 404]:
                print(f"Error {err.resp.status}: {err}")
                print("Check spreadsheet ID and service account permissions.")
                sys.exit(1)
            elif attempt < MAX_RETRIES - 1:
                print(f"Attempt {attempt + 1} failed. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed after {MAX_RETRIES} attempts: {err}")
                sys.exit(1)

def main():
    creds = setup_credentials()
    service = build("sheets", "v4", credentials=creds)
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')

    print(f"Attempting to access spreadsheet with ID: {spreadsheet_id}")

    csv_content = read_csv('public/merged.csv')
    if not validate_data(csv_content):
        sys.exit(1)

    upload_to_sheets(service, spreadsheet_id, csv_content)

if __name__ == "__main__":
    main()
