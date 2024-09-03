# This file contains the filter view related functions from adjust_column_widths.py

def create_filter_view():
    """
    Create a filter view for the sheet.
    This function was previously part of adjust_column_widths.py.
    """
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
    """
    Delete existing filter view if it exists.
    """
    try:
        # Get the current filter views
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        
        for sheet in sheets:
            filter_views = sheet.get('filterViews', [])
            for filter_view in filter_views:
                if filter_view.get('title') == filter_title:
                    # Delete the filter view
                    request = {
                        "deleteFilterView": {
                            "filterId": filter_view['filterViewId']
                        }
                    }
                    body = {'requests': [request]}
                    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
                    print(f"Deleted existing filter view: {filter_title}")
                    return

        print(f"No existing filter view found with title: {filter_title}")
    except Exception as e:
        print(f"Error deleting filter view: {e}")
