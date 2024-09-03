import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

def create_conditional_formatting_rules():
    """Create conditional formatting rules for the sheet with updated colors."""
    return [
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 50000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {"userEnteredValue": '=$A2="new"'}
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.7,
                                "green": 0.9,
                                "blue": 0.7
                            }
                        }
                    }
                },
                "index": 0
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 50000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {"userEnteredValue": '=$A2="hot"'}
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 1.0,
                                "green": 0.8,
                                "blue": 0.4
                            }
                        }
                    }
                },
                "index": 1
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 50000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {"userEnteredValue": '=$A2="recent"'}
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.6,
                                "green": 0.8,
                                "blue": 1.0
                            }
                        }
                    }
                },
                "index": 2
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 50000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {"userEnteredValue": '=$A2="aging"'}
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.95,
                                "green": 0.95,
                                "blue": 0.95
                            }
                        }
                    }
                },
                "index": 3
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 50000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {"userEnteredValue": '=$A2="old"'}
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.9,
                                "green": 0.9,
                                "blue": 0.9
                            }
                        }
                    }
                },
                "index": 4
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 50000,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [
                                {"userEnteredValue": '=$A2="expired"'}
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.85,
                                "green": 0.85,
                                "blue": 0.85
                            }
                        }
                    }
                },
                "index": 5
            }
        }
    ]

def create_filter_view():
    """Create a filter view for the sheet."""
    return {
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 50000,
                    "startColumnIndex": 0,
                    "endColumnIndex": 16
                },
                "criteria": {
                    "0": {
                        "hiddenValues": ["expired"]
                    }
                }
            }
        }
    }

def delete_existing_filter_view(service, spreadsheet_id, filter_title):
    """Delete existing filter view if it exists."""
    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet = spreadsheet['sheets'][0]
        sheet_id = sheet['properties']['sheetId']
        filter_views = sheet.get('filterViews', [])
        for filter_view in filter_views:
            if filter_view['title'] == filter_title:
                filter_view_id = filter_view['filterViewId']
                service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={
                        "requests": [
                            {
                                "deleteFilterView": {
                                    "filterId": filter_view_id
                                }
                            }
                        ]
                    }
                ).execute()
                print(f"Deleted existing filter view: {filter_title}")
                return
    except HttpError as err:
        print(f"Error deleting filter view: {err}")
        raise

def create_filter_on_first_row():
    """Create a filter on the first row of the sheet with condition to hide 'expired' in 'job_age'."""
    return {
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 16
                },
                "criteria": {
                    "0": {
                        "hiddenValues": ["expired"]
                    }
                }
            }
        }
    }

def adjust_column_widths(spreadsheet_id):
    """Adjust column widths, add conditional formatting, and create filter view."""
    creds = setup_credentials()
    service = build("sheets", "v4", credentials=creds)

    column_widths = {
        'job_age': 78,
        'company': 467,
        'job_title': 650,
        'job_type': 82,
        'job_location': 344,
        'job_department': 548,
        'job_url': 662,
        'first_seen': 131,
        'base_salary': 303,
        'job_level': 96,
        'job_apply_end_date': 156,
        'last_seen': 131,
        'is_active': 83,
        'company_url': 646,
        'job_board': 136,
        'job_board_url': 244
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

    requests.extend(create_conditional_formatting_rules())
    delete_existing_filter_view(service, spreadsheet_id, "Filter by Job Age")
    requests.append(create_filter_view())

    body = {"requests": requests}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print("Column widths, conditional formatting, and filter view adjusted successfully.")

if __name__ == "__main__":
    spreadsheet_id = get_env_var('GOOGLE_SHEETS_ID_DEV')
    adjust_column_widths(spreadsheet_id)