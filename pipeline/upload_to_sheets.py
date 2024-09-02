import os
import requests
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
    scopes: list
    sheet_range: str
    max_retries: int
    sheet_id: int

config = Config(
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
    sheet_range="Sheet1!A1:Z1000",
    max_retries=5,
    sheet_id=0
)

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

# Fetch and save the regions JSON for future use
def fetch_and_save_regions_json():
    url = 'https://raw.githubusercontent.com/mtegarsantosa/json-nama-daerah-indonesia/master/regions.json'
    response = requests.get(url)
    regions = response.json()

    os.makedirs('output', exist_ok=True)
    with open('output/regions.json', 'w') as f:
        json.dump(regions, f)

# Load the regions JSON from the output folder for future use
def load_regions_json():
    with open('output/regions.json', 'r') as f:
        return json.load(f)

# Sanitize job location by using the regions JSON
# This function needs more R&D for future use
def sanitize_job_location(job_location):
    """
    Sanitize job location by using json from the output folder
    and replace the job location with the corresponding name from the json.

    Args:
        job_location (str): The job location value.

    Returns:
        str: The sanitized job location value.
    """
    if pd.isna(job_location):
        return 'N/A'
    
    regions = load_regions_json()

    # Replace English direction words with Bahasa equivalents
    direction_map = {
        "west": "barat",
        "east": "timur",
        "north": "utara",
        "south": "selatan"
    }
    for eng, bahasa in direction_map.items():
        job_location = job_location.replace(eng, bahasa)

    for region in regions:
        for kota in region['kota']:
            if kota in job_location:
                if "Kab." in job_location or "Kota" in job_location:
                    return kota
                else:
                    return f"Kota {kota}"
        if region['provinsi'] in job_location:
            return f"Kota {region['provinsi']}"

    return job_location

def read_csv(file_path):
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
        # Commented out for future use
        # df['job_location'] = df['job_location'].apply(sanitize_job_location)
        df = df.fillna('')
        df = df.astype(str).apply(lambda x: x.str.strip())
        return [df.columns.tolist()] + df.values.tolist()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path}")
        sys.exit(1)

def validate_data(data):
    if not data or len(data) < 2:
        print("Error: CSV data is empty or has insufficient rows")
        return False
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

def sanitize_job_type(job_type):
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

def main():
    # Fetch and save the regions JSON for future use
    # fetch_and_save_regions_json()

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