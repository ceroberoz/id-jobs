import os
import json
import sys
import time
import random
import logging
from dataclasses import dataclass
from contextlib import contextmanager
from typing import List, Dict, Any

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Config:
    scopes: tuple = ("https://www.googleapis.com/auth/spreadsheets",)
    max_retries: int = 3
    sheet_range: str = 'Sheet1'
    sheet_id: int = 0  # Assumes first sheet in the spreadsheet
    csv_file_path: str = 'output/merged.csv'

config = Config()

def get_env_var(var_name: str) -> str:
    value = os.environ.get(var_name)
    if not value:
        logger.error(f"{var_name} environment variable is not set or is empty")
        sys.exit(1)
    return value

def setup_credentials():
    gcp_json = get_env_var('GCP_JSON')
    try:
        creds_dict = json.loads(gcp_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict, scopes=config.scopes)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in GCP_JSON environment variable")
        sys.exit(1)

def read_csv(file_path: str) -> List[List[str]]:
    try:
        df = pd.read_csv(file_path, dtype={'job_type': str})
        columns = df.columns.tolist()
        columns.insert(0, columns.pop(columns.index('company')))
        job_type_index = columns.index('job_type')
        job_title_index = columns.index('job_title')
        columns.insert(job_title_index + 1, columns.pop(job_type_index))
        df = df[columns]

        df['job_type'] = df['job_type'].apply(sanitize_job_type)
        df = df.fillna('')
        df = df.astype(str).apply(lambda x: x.str.strip())
        return [df.columns.tolist()] + df.values.tolist()
    except FileNotFoundError:
        logger.error(f"CSV file not found at {file_path}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logger.error(f"CSV file is empty: {file_path}")
        sys.exit(1)

def validate_data(data: List[List[str]]) -> bool:
    if not data or len(data) < 2:
        logger.error("CSV data is empty or has insufficient rows")
        return False
    # Add more validation as needed
    return True

def clean_data(data: List[List[str]]) -> List[List[str]]:
    return [[str(cell).replace('\n', ' ').strip() for cell in row] for row in data]

@contextmanager
def get_sheets_service(creds):
    service = build("sheets", "v4", credentials=creds)
    try:
        yield service
    finally:
        service.close()

def upload_to_sheets(service, spreadsheet_id: str, data: List[List[str]]):
    body = {'values': data}

    for attempt in range(config.max_retries):
        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            logger.info(f"Successfully accessed spreadsheet: {spreadsheet['properties']['title']}")

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
            logger.info(f"{result.get('updatedCells')} cells updated.")

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

            logger.info("Header row formatted as bold and frozen.")
            return
        except HttpError as err:
            if err.resp.status in [403, 404]:
                logger.error(f"Error {err.resp.status}: {err}")
                logger.error("Check spreadsheet ID and service account permissions.")
                sys.exit(1)
            elif attempt < config.max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Attempt {attempt + 1} failed. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Failed after {config.max_retries} attempts: {err}")
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
    try:
        creds = setup_credentials()
        spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')

        logger.info(f"Attempting to access spreadsheet with ID: {spreadsheet_id}")

        csv_content = read_csv(config.csv_file_path)
        if not validate_data(csv_content):
            sys.exit(1)

        cleaned_content = clean_data(csv_content)

        with get_sheets_service(creds) as service:
            upload_to_sheets(service, spreadsheet_id, cleaned_content)
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()