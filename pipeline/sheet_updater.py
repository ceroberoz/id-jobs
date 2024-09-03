# This file contains the main functionality from adjust_column_widths.py
# It uses the other modules to perform the sheet updates

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Remove or comment out this line:
# sys.path.append(str(Path(__file__).parent.parent))

# Replace the imports with consistent relative imports:
from pipeline.column_widths import get_column_widths
from pipeline.conditional_formatting import create_conditional_formatting_rules
from pipeline.filter_view import create_filter_view, delete_existing_filter_view

def get_env_var(var_name):
    """Retrieve environment variable or raise an error if not set."""
    value = os.environ.get(var_name)
    if not value:
        raise ValueError(f"{var_name} environment variable is not set or is empty")
    return value

def setup_credentials():
    """Setup Google Sheets API credentials."""
    gcp_json = get_env_var('GCP_JSON')
    try:
        creds_dict = json.loads(gcp_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in GCP_JSON environment variable")

def adjust_column_widths(spreadsheet_id):
    """
    Adjust column widths, add conditional formatting, and create filter view.
    This function combines the main functionality from adjust_column_widths.py,
    but now uses the separate modules for each part of the process.
    """
    creds = setup_credentials()
    service = build("sheets", "v4", credentials=creds)

    column_widths = get_column_widths()

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

    requests.extend(create_conditional_formatting_rules())
    delete_existing_filter_view(service, spreadsheet_id, "Filter by Job Age")
    requests.append(create_filter_view())

    body = {"requests": requests}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print("Column widths, conditional formatting, and filter view adjusted successfully.")

def clear_sheet(service, spreadsheet_id):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    properties = sheet_metadata.get('sheets', [])[0].get('properties', {})
    sheet_id = properties.get('sheetId', 0)

    requests = [{
        "updateCells": {
            "range": {
                "sheetId": sheet_id,
            },
            "fields": "userEnteredValue"
        }
    }]

    body = {
        'requests': requests
    }
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print("Sheet cleared successfully.")

if __name__ == "__main__":
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID_DEV')
    adjust_column_widths(spreadsheet_id)
