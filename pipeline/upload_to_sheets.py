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
    """
    Configuration class for the Google Sheets API.

    Attributes:
        scopes (tuple): The scopes required for the API.
        max_retries (int): The maximum number of retries for API calls.
        sheet_range (str): The range of the sheet to update.
        sheet_id (int): The ID of the sheet to update.
    """
    scopes: tuple = ("https://www.googleapis.com/auth/spreadsheets",)
    max_retries: int = 3
    sheet_range: str = 'Sheet1'
    sheet_id: int = 0  # Assumes first sheet in the spreadsheet

config = Config()

def get_env_var(var_name):
    """
    Retrieve environment variable or exit if not set.

    Args:
        var_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.
    """
    value = os.environ.get(var_name)
    if not value:
        print(f"Error: {var_name} environment variable is not set or is empty")
        sys.exit(1)
    return value

def setup_credentials():
    """
    Setup Google Sheets API credentials.

    Returns:
        google.oauth2.service_account.Credentials: The credentials object.
    """
    gcp_json = get_env_var('GCP_JSON')
    try:
        creds_dict = json.loads(gcp_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict, scopes=config.scopes)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in GCP_JSON environment variable")
        sys.exit(1)

def read_csv(file_path):
    """
    Read and preprocess CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: The preprocessed CSV data.
    """
    try:
        df = pd.read_csv(file_path, dtype={'job_type': str})
        columns = df.columns.tolist()
        columns.insert(0, columns.pop(columns.index('job_age')))
        columns.insert(1, columns.pop(columns.index('company')))
        job_type_index = columns.index('job_type')
        job_title_index = columns.index('job_title')
        columns.insert(job_title_index + 1, columns.pop(job_type_index))
        df = df[columns]
        df['job_type'] = df['job_type'].apply(sanitize_job_type)
        df = df.fillna('')
        df = df.astype(str).apply(lambda x: x.str.strip())
        return [df.columns.tolist()] + df.values.tolist()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        sys.exit(1)

def validate_data(data):
    """
    Validate CSV data.

    Args:
        data (list): The CSV data.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not data or len(data) < 2:
        print("Error: CSV data is empty or has insufficient rows")
        return False
    return True

def clean_data(data):
    """
    Clean CSV data.

    Args:
        data (list): The CSV data.

    Returns:
        list: The cleaned CSV data.
    """
    return [[str(cell).replace('\n', ' ').strip() for cell in row] for row in data]

@contextmanager
def get_sheets_service(creds):
    """
    Context manager for Google Sheets service.

    Args:
        creds (google.oauth2.service_account.Credentials): The credentials object.

    Yields:
        googleapiclient.discovery.Resource: The Google Sheets service.
    """
    service = build("sheets", "v4", credentials=creds)
    try:
        yield service
    finally:
        service.close()

def upload_to_sheets(service, spreadsheet_id, data):
    """
    Upload data to Google Sheets.

    Args:
        service (googleapiclient.discovery.Resource): The Google Sheets service.
        spreadsheet_id (str): The ID of the spreadsheet.
        data (list): The data to upload.
    """
    body = {'values': data}
    for attempt in range(config.max_retries):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            print(f"Successfully accessed spreadsheet: {spreadsheet['properties']['title']}")

            service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=config.sheet_range
            ).execute()

            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=config.sheet_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"{result.get('updatedCells')} cells updated.")

            format_header_and_freeze(service, spreadsheet_id)
            return
        except HttpError as err:
            handle_http_error(err, attempt)

def format_header_and_freeze(service, spreadsheet_id):
    """
    Format header row as bold and freeze it.

    Args:
        service (googleapiclient.discovery.Resource): The Google Sheets service.
        spreadsheet_id (str): The ID of the spreadsheet.
    """
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
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    ).execute()
    print("Header row formatted as bold and frozen.")

def handle_http_error(err, attempt):
    """
    Handle HTTP errors with retries.

    Args:
        err (googleapiclient.errors.HttpError): The HTTP error.
        attempt (int): The current attempt number.
    """
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
    """
    Main function to upload CSV data to Google Sheets.
    """
    creds = setup_credentials()
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID_DEV')
    print(f"Attempting to access spreadsheet with ID: {spreadsheet_id}")
    csv_content = read_csv('output/merged.csv')
    if not validate_data(csv_content):
        sys.exit(1)
    cleaned_content = clean_data(csv_content)
    with get_sheets_service(creds) as service:
        upload_to_sheets(service, spreadsheet_id, cleaned_content)

def sanitize_job_type(job_type):
    """
    Sanitize job type values.

    Args:
        job_type (str): The job type value.

    Returns:
        str: The sanitized job type value.
    """
    if pd.isna(job_type):
        return ''
    job_type = str(job_type).replace(',', ' & ')
    contract_types = {'contract', 'contract & fullTime', 'Contractual', 'Kontrak'}
    freelance_types = {'freelance'}
    part_time_types = {'Part time', 'partTime', 'Paruh waktu'}
    full_time_types = {'Full Time', 'fullTime', 'fullTime & Contract', 'fullTime & freelance'}
    internship_types = {'Intern', 'internship'}
    job_type_lower = job_type.lower()
    if any(t.lower() in job_type_lower for t in contract_types):
        return 'Contract'
    elif any(t.lower() in job_type_lower for t in freelance_types):
        return 'Freelance'
    elif any(t.lower() in job_type_lower for t in part_time_types):
        return 'Part time'
    elif any(t.lower() in job_type_lower for t in full_time_types):
        return 'Full time'
    elif any(t.lower() in job_type_lower for t in internship_types):
        return 'Internship'
    else:
        return job_type

if __name__ == "__main__":
    main()