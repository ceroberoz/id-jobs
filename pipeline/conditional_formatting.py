# This file contains the conditional formatting rules from adjust_column_widths.py

def create_conditional_formatting_rules():
    """
    Create conditional formatting rules for the sheet with updated colors.
    This function was previously part of adjust_column_widths.py.
    """
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
