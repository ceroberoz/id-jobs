import os
import json
import sys
import time
import random
import re
from datetime import datetime
from dataclasses import dataclass
from contextlib import contextmanager
from dotenv import load_dotenv

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    scopes: list
    sheet_range: str
    max_retries: int
    sheet_id: int

config = Config(
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
    sheet_range="",  # This will be set dynamically later
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

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path, dtype={'job_type': str, 'job_level': str})
        desired_order = [
            'job_age', 'company', 'work_arrangement', 'job_title', 'job_type', 'job_department',
            'job_location', 'job_url', 'base_salary', 'job_level', 'first_seen',
            'last_seen', 'job_apply_end_date', 'is_active', 'job_board', 'company_url', 'job_board_url'
        ]
        for col in desired_order:
            if col not in df.columns:
                df[col] = ''
        df = df[desired_order]
        df = df.fillna('Not specified')
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
    header = data[0]
    cleaned_data = [header]

    for row in data[1:]:
        cleaned_row = []
        for i, cell in enumerate(row):
            cell = str(cell).strip()

            if cell in ('', 'N/A', 'nan'):
                cell = 'Not specified'

            if header[i] in ('first_seen', 'last_seen', 'job_apply_end_date'):
                cell = standardize_date(cell)

            if header[i] == 'job_title':
                cell = clean_job_title(cell)

            if header[i] == 'job_location':
                cell = normalize_location(cell)

            if header[i] == 'job_type':
                cell = sanitize_job_type(cell)

            if header[i] == 'work_arrangement':
                cell = sanitize_work_arrangement(cell)

            if header[i] == 'job_level':
                cell = sanitize_job_level(cell)

            if header[i] == 'job_department':
                cell = sanitize_job_department(cell)

            if header[i] == 'is_active':
                cell = 'True' if cell.lower() == 'true' else 'False'

            if header[i] == 'company':
                cell = cell.strip()

            if 'url' in header[i]:
                cell = validate_url(cell)

            cleaned_row.append(cell)

        cleaned_data.append(cleaned_row)

    return cleaned_data

def standardize_date(date_str):
    if date_str in ('Not specified', 'nan'):
        return 'Not specified'
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return 'Invalid date'

def clean_job_title(title):
    title = re.sub(r'^(Jr\.|Senior|Sr\.) ', '', title)
    title = re.sub(r' (I|II|III|IV|V)$', '', title)
    return title.strip()

def normalize_location(location):
    return location.split(',')[0].strip()

def validate_url(url):
    if url.startswith(('http://', 'https://')):
        return url
    return 'Invalid URL'

def sanitize_job_type(job_type):
    if job_type in ('Not specified', 'nan'):
        return 'Not specified'

    job_type = str(job_type).lower()

    contract_types = {'contract', 'contract & fulltime', 'contractual', 'kontrak', 'fixed term employment'}
    freelance_types = {'freelance'}
    part_time_types = {'part time', 'parttime', 'paruh waktu', 'part-time'}
    full_time_types = {'full time', 'fulltime', 'fulltime & contract', 'fulltime & freelance', 'full-time'}
    internship_types = {'intern', 'internship', 'magang'}
    permanent_types = {'permanent', 'permanent employment'}
    consultant_types = {'consultant'}
    casual_types = {'kasual', 'casual'}
    partnership_types = {'partnership'}

    if any(t in job_type for t in contract_types):
        return 'Contract'
    elif any(t in job_type for t in freelance_types):
        return 'Freelance'
    elif any(t in job_type for t in part_time_types):
        return 'Part time'
    elif any(t in job_type for t in full_time_types):
        return 'Full time'
    elif any(t in job_type for t in internship_types):
        return 'Internship'
    elif any(t in job_type for t in permanent_types):
        return 'Permanent'
    elif any(t in job_type for t in consultant_types):
        return 'Consultant'
    elif any(t in job_type for t in casual_types):
        return 'Casual'
    elif any(t in job_type for t in partnership_types):
        return 'Partnership'
    else:
        return job_type.capitalize()

def sanitize_work_arrangement(arrangement):
    if arrangement in ('Not specified', 'nan', 'False'):
        return 'Not specified'

    arrangement = str(arrangement).lower()

    remote_types = {'remote', 'jarak jauh', 'work from home', 'wfh'}
    hybrid_types = {'hybrid', 'hibrid'}
    onsite_types = {'onsite', 'on-site', 'kantor', 'office'}

    types = []
    if any(t in arrangement for t in remote_types):
        types.append('Remote')
    if any(t in arrangement for t in hybrid_types):
        types.append('Hybrid')
    if any(t in arrangement for t in onsite_types):
        types.append('On-site')

    if types:
        return ' / '.join(types)
    elif arrangement == 'full-time':
        return 'On-site'
    else:
        return arrangement.capitalize()

def sanitize_job_level(job_level):
    if job_level in ('Not specified', 'nan'):
        return 'Not specified'

    job_level = str(job_level).lower()

    entry_level = {'fresh graduate', 'intern', 'internship', 'undergraduate', 'entry level', 'junior'}
    mid_level = {'specialist', 'professional', 'lead', 'mid level', 'intermediate'}
    senior_level = {'senior', 'senior officer', 'expert'}
    manager_level = {'manager', 'supervisor', 'team lead'}
    director_level = {'director', 'head', 'head of department', 'vp', 'vice president'}
    executive_level = {'c-level', 'executive', 'ceo', 'cto', 'cfo'}

    if any(level in job_level for level in entry_level):
        return 'Entry Level'
    elif any(level in job_level for level in mid_level):
        return 'Mid Level'
    elif any(level in job_level for level in senior_level):
        return 'Senior Level'
    elif any(level in job_level for level in manager_level):
        return 'Manager'
    elif any(level in job_level for level in director_level):
        return 'Director'
    elif any(level in job_level for level in executive_level):
        return 'Executive'
    else:
        return job_level.capitalize()

def sanitize_job_department(department):
    department_mapping = {
        '2000160518': 'Marketing',
        '2000160519': 'Finance',
        '2000160520': 'Operations',
        '2000160726': 'Product',
        '2000175832': 'Legal & Compliance',
        '2000178745': 'Engineering',
        '2000179058': 'People',
        '2000179132': 'Fraud Management'
    }

    if department in ('Not specified', 'nan'):
        return 'Not specified'

    department = str(department).strip()

    if department in department_mapping:
        return department_mapping[department]

    # If the department is not in the mapping, return it as is (capitalized)
    return department.capitalize()

@contextmanager
def get_sheets_service(creds):
    service = build("sheets", "v4", credentials=creds)
    try:
        yield service
    finally:
        service.close()

def get_dynamic_range(data):
    num_rows = len(data)
    num_cols = len(data[0]) if data else 0
    return f"Sheet1!A1:{chr(65 + num_cols - 1)}{num_rows}"

def upload_to_sheets(service, spreadsheet_id, data):
    config.sheet_range = get_dynamic_range(data)
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
