import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up credentials
creds = service_account.Credentials.from_service_account_info(
    eval(os.environ['GCP_SA_KEY']),
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=creds)

# Get the Sheet ID from environment variable
SHEET_ID = os.environ['SHEET_ID']

# Read the existing merged CSV file
csv_file = 'public/merged.csv'
df = pd.read_csv(csv_file)

# Convert DataFrame to list of lists
values = [df.columns.tolist()] + df.values.tolist()

# Sheet name
sheet_name = 'Merged Jobs'

# Update or create sheet
try:
    # Try to clear existing content
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range=f'{sheet_name}!A1:Z'
    ).execute()
except:
    # If sheet doesn't exist, add a new one
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

print("Google Sheets updated successfully with merged data!")
