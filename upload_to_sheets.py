import os
import csv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, update the GCP_JSON secret accordingly.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"{var_name} environment variable is not set")
    return value

def setup_credentials():
    gcp_json = get_env_var('GCP_JSON')
    creds_dict = json.loads(gcp_json)
    return service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES)

def read_csv(file_path):
    with open(file_path, 'r') as file:
        return list(csv.reader(file))

def upload_to_sheets(service, spreadsheet_id, data):
    sheet_range = 'Sheet1'  # Update this if you want to use a different sheet name
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
    except HttpError as err:
        print(f"An error occurred: {err}")
        raise

def main():
    try:
        creds = setup_credentials()
        service = build("sheets", "v4", credentials=creds)
        spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')

        csv_content = read_csv('public/merged.csv')
        upload_to_sheets(service, spreadsheet_id, csv_content)
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
