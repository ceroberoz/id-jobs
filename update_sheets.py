import os
import sys
import json
from datetime import datetime

try:
    import pandas as pd
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError as e:
    print(f"Error: {e}. Please make sure all required packages are installed.")
    sys.exit(1)

# Set up credentials
try:
    gcp_sa_key = os.environ['GCP_SA_KEY']
    service_account_info = json.loads(gcp_sa_key)
    creds = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
except KeyError:
    print("Error: GCP_SA_KEY environment variable not set.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON in GCP_SA_KEY environment variable.")
    sys.exit(1)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=creds)

# Get the Sheet ID from environment variable
SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')
if not SHEET_ID:
    print("Error: GOOGLE_SHEET_ID environment variable not set or empty.")
    sys.exit(1)

print(f"Using Sheet ID: {SHEET_ID}")

# Read the existing merged CSV file
csv_file = 'public/merged.csv'
try:
    df = pd.read_csv(csv_file)
    if df.empty:
        raise ValueError("CSV file is empty")
except FileNotFoundError:
    print(f"Error: CSV file '{csv_file}' not found.")
    sys.exit(1)
except (pd.errors.EmptyDataError, ValueError):
    print(f"Error: CSV file '{csv_file}' is empty.")
    sys.exit(1)
except pd.errors.ParserError:
    print(f"Error: Unable to parse CSV file '{csv_file}'.")
    sys.exit(1)

# Convert DataFrame to list of lists
values = [df.columns.tolist()] + df.values.tolist()

# Sheet name with current date
current_date = datetime.now().strftime("%Y-%m-%d")
sheet_name = f'Jobs {current_date}'

# Update or create sheet
try:
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheet_exists = any(sheet['properties']['title'] == sheet_name for sheet in sheets)

    if sheet_exists:
        service.spreadsheets().values().clear(
            spreadsheetId=SHEET_ID,
            range=f'{sheet_name}!A1:Z'
        ).execute()
    else:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={'requests': [{'addSheet': {'properties': {'title': sheet_name}}}]}
        ).execute()

    # Update sheet with new data
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f'{sheet_name}!A1',
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
    print(f"Google Sheets updated successfully with merged data in sheet: {sheet_name}")

except HttpError as e:
    print(f"HTTP Error occurred: {e}")
    print(f"Response content: {e.content}")
    sys.exit(1)
except Exception as e:
    print(f"Error updating Google Sheets: {e}")
    sys.exit(1)
