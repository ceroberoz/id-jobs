import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise ValueError(f"{var_name} environment variable is not set or is empty")
    return value

def setup_credentials():
    gcp_json = get_env_var('GCP_JSON')
    creds_dict = json.loads(gcp_json)
    return service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])

def adjust_column_widths(spreadsheet_id):
    creds = setup_credentials()
    service = build("sheets", "v4", credentials=creds)

    column_widths = {
        'job_title': 684,
        'job_location': 255,
        'job_department': 548,
        'job_url': 662,
        'first_seen': 130,
        'base_salary': 304,
        'job_type': 112,
        'job_level': 64,
        'job_apply_end_date': 225,
        'last_seen': 170,
        'is_active': 63,
        'company': 467,
        'company_url': 646,
        'job_board': 72,
        'job_board_url': 213
    }

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

    body = {"requests": requests}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print("Column widths adjusted successfully.")

if __name__ == "__main__":
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID')
    adjust_column_widths(spreadsheet_id)
