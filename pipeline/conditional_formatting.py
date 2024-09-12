# This file contains the conditional formatting rules from adjust_column_widths.py

def create_conditional_formatting_rules():
    return [
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 50000, "startColumnIndex": 0, "endColumnIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$A2="new"'}]},
                        "format": {"backgroundColor": {"red": 0.0, "green": 0.8, "blue": 0.0}}  # Bright Green
                    }
                },
                "index": 0
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 50000, "startColumnIndex": 0, "endColumnIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$A2="hot"'}]},
                        "format": {"backgroundColor": {"red": 1.0, "green": 0.4, "blue": 0.0}}  # Bright Orange
                    }
                },
                "index": 1
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 50000, "startColumnIndex": 0, "endColumnIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$A2="recent"'}]},
                        "format": {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 0.0}}  # Bright Yellow
                    }
                },
                "index": 2
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 50000, "startColumnIndex": 0, "endColumnIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$A2="aging"'}]},
                        "format": {"backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}}  # Light Gray
                    }
                },
                "index": 3
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 50000, "startColumnIndex": 0, "endColumnIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$A2="old"'}]},
                        "format": {"backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}  # Medium Gray
                    }
                },
                "index": 4
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 50000, "startColumnIndex": 0, "endColumnIndex": 1}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$A2="expired"'}]},
                        "format": {"backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7}}  # Dark Gray
                    }
                },
                "index": 5
            }
        }
    ]
