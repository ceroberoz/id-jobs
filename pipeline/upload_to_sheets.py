import os
import json
import sys
import time
import random
from dataclasses import dataclass
from contextlib import contextmanager

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

@dataclass
class Config:
    scopes: tuple = ("https://www.googleapis.com/auth/spreadsheets",)
    max_retries: int = 3
    sheet_range: str = 'Sheet1'
    sheet_id: int = 0  # Assumes first sheet in the spreadsheet

config = Config()

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
            creds_dict, scopes=config.scopes)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in GCP_JSON environment variable")
        sys.exit(1)

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # Replace NaN values with empty strings
        df = df.fillna('')
        # Convert all values to strings and strip whitespace
        df = df.astype(str).apply(lambda x: x.str.strip())
        return [df.columns.tolist()] + df.values.tolist()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        sys.exit(1)

def validate_data(data):
    if not data or len(data) < 2:  # Check for header and at least one data row
        print("Error: CSV data is empty or has insufficient rows")
        return False
    # Add more validation as needed
    return True

def clean_data(data):
    return [[str(cell).replace('\n', ' ').strip() for cell in row] for row in data]

@contextmanager
def get_sheets_service(creds):
    service = build("sheets", "v4", credentials=creds)
    try:
        yield service
    finally:
        service.close()

def upload_to_sheets(service, spreadsheet_id, data):
    body = {'values': data}

    for attempt in range(config.max_retries):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            print(f"Successfully accessed spreadsheet: {spreadsheet['properties']['title']}")

            # Clear the sheet
            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=config.sheet_range
            ).execute()

            # Update values
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=config.sheet_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"{result.get('updatedCells')} cells updated.")

            # Format header row as bold and freeze it
            requests = [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": config.sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat.textFormat.bold"
                    }
                },
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": config.sheet_id,
                            "gridProperties": {
                                "frozenRowCount": 1
                            }
                        },
                        "fields": "gridProperties.frozenRowCount"
                    }
                }
            ]

            # Execute the formatting requests
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": requests}
            ).execute()

            print("Header row formatted as bold and frozen.")
            return
        except HttpError as err:
            if err.resp.status in [403, 404]:
                print(f"Error {err.resp.status}: {err}")
                print("Check spreadsheet ID and service account permissions.")
                sys.exit(1)
            elif attempt < config.max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {config.max_retries} attempts: {err}")
                sys.exit(1)

def main():
    creds = setup_credentials()
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')

    print(f"Attempting to access spreadsheet with ID: {spreadsheet_id}")

    csv_content = read_csv('output/merged.csv')
    if not validate_data(csv_content):
        sys.exit(1)

    cleaned_content = clean_data(csv_content)

    with get_sheets_service(creds) as service:
        upload_to_sheets(service, spreadsheet_id, cleaned_content)

if __name__ == "__main__":
    main()
