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
    csv_directory: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

    @staticmethod
    def get_column_widths() -> Dict[str, int]:
        return {
            'company': 467,
            'job_title': 684,
            'job_type': 112,
            'job_location': 255,
            'job_department': 548,
            'job_url': 662,
            'first_seen': 130,
            'base_salary': 304,
            'job_level': 64,
            'job_apply_end_date': 225,
            'last_seen': 170,
            'is_active': 63,
            'job_board': 72,
            'job_board_url': 213
        }

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

def read_csv_files(directory: str) -> List[List[str]]:
    all_data = []
    header = None
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    if not csv_files:
        logger.error(f"No CSV files found in {directory}")
        sys.exit(1)
    
    for file in csv_files:
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path, dtype={'job_type': str})
            if header is None:
                header = df.columns.tolist()
                header.insert(0, header.pop(header.index('company')))
                job_type_index = header.index('job_type')
                job_title_index = header.index('job_title')
                header.insert(job_title_index + 1, header.pop(job_type_index))
                all_data.append(header)
            
            df = df[header]
            df['job_type'] = df['job_type'].apply(sanitize_job_type)
            df = df.fillna('')
            df = df.astype(str).apply(lambda x: x.str.strip())
            all_data.extend(df.values.tolist())
            logger.info(f"Successfully processed {file}")
        except pd.errors.EmptyDataError:
            logger.warning(f"CSV file is empty: {file_path}")
        except Exception as e:
            logger.error(f"Error processing {file}: {str(e)}")
    
    if not all_data:
        logger.error("No data found in any CSV files")
        sys.exit(1)
    
    return all_data

def validate_data(data: List[List[str]]) -> bool:
    if not data or len(data) < 2:
        logger.error("CSV data is empty or has insufficient rows")
        return False
    expected_columns = set(config.get_column_widths().keys())
    actual_columns = set(data[0])
    if not expected_columns.issubset(actual_columns):
        missing_columns = expected_columns - actual_columns
        logger.error(f"Missing columns in CSV data: {', '.join(missing_columns)}")
        return False
    return True

def clean_data(data: List[List[str]]) -> List[List[str]]:
    return [[str(cell).replace('\n', ' ').strip() for cell in row] for row in data]

@contextmanager
def get_sheets_service(creds):
    try:
        service = build('sheets', 'v4', credentials=creds)
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

        csv_content = read_csv_files(config.csv_directory)
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