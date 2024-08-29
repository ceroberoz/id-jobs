import os
import json
import logging
from typing import Dict, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_env_var(var_name: str) -> str:
    value = os.environ.get(var_name)
    if not value:
        raise ValueError(f"{var_name} environment variable is not set or is empty")
    return value

def setup_credentials():
    gcp_json = get_env_var('GCP_JSON')
    try:
        creds_dict = json.loads(gcp_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    except json.JSONDecodeError:
        logger.error("Invalid JSON in GCP_JSON environment variable")
        raise

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

def create_update_requests(column_widths: Dict[str, int]) -> List[Dict]:
    requests = []
    for index, (column_name, width) in enumerate(column_widths.items()):
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": index,
                    "endIndex": index + 1
                },
                "properties": {
                    "pixelSize": width
                },
                "fields": "pixelSize"
            }
        })
    return requests

def adjust_column_widths(spreadsheet_id: str):
    try:
        creds = setup_credentials()
        service = build("sheets", "v4", credentials=creds)

        column_widths = get_column_widths()
        requests = create_update_requests(column_widths)

        body = {"requests": requests}
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        logger.info("Column widths adjusted successfully.")
    except HttpError as err:
        logger.error(f"An error occurred: {err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise

def main():
    try:
        spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')
        adjust_column_widths(spreadsheet_id)
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()