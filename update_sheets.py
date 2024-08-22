import os
import sys

try:
    import pandas as pd
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError as e:
    print(f"Error: {e}. Please make sure all required packages are installed.")
    sys.exit(1)

# Set up credentials
gcp_sa_key = os.environ.get('GCP_SA_KEY')
if not gcp_sa_key:
    raise ValueError("GCP_SA_KEY environment variable is not set")

try:
    service_account_info = json.loads(gcp_sa_key)
except json.JSONDecodeError:
    raise ValueError("GCP_SA_KEY is not a valid JSON string")

creds = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# Build the Sheets API service
service = build('sheets', 'v4', credentials=creds)

# Get the Sheet ID from environment variable
SHEET_ID = os.environ.get('SHEET_ID')
if not SHEET_ID:
    raise ValueError("SHEET_ID environment variable is not set")

# Read the existing merged CSV file
csv_file = 'public/merged.csv'
df = pd.read_csv(csv_file)

# Convert DataFrame to list of lists
values = [df.columns.tolist()] + df.values.tolist()

# Generate sheet name with current date
current_date = datetime.date.today().strftime("%Y-%m-%d")
sheet_name = f"{current_date} - id-jobs"

# Update or create sheet
try:
    # Try to clear existing content
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range=f'{sheet_name}!A1:Z'
    ).execute()
except Exception as e:
    print(f"Error clearing sheet: {e}")
    # If sheet doesn't exist, add a new one
    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={'requests': [{'addSheet': {'properties': {'title': sheet_name}}}]}
        ).execute()
    except Exception as e:
        print(f"Error creating new sheet: {e}")
        raise

# Update sheet with new data
try:
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f'{sheet_name}!A1',
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
    print("Google Sheets updated successfully with merged data!")
except Exception as e:
    print(f"Error updating sheet: {e}")
    raise
