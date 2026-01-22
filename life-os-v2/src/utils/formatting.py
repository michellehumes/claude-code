"""
Formatting utilities for Life OS v2 Google Sheets
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, NUMBER_FORMATS


def create_header_format():
    """Create standard header row format"""
    return {
        "backgroundColor": COLORS["header_bg"],
        "textFormat": {
            "foregroundColor": COLORS["header_text"],
            "bold": True,
            "fontSize": 11,
            "fontFamily": "Arial"
        },
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    }


def create_currency_format():
    """Create currency number format"""
    return {
        "numberFormat": {
            "type": "CURRENCY",
            "pattern": NUMBER_FORMATS["currency"]
        }
    }


def create_percentage_format():
    """Create percentage number format"""
    return {
        "numberFormat": {
            "type": "PERCENT",
            "pattern": NUMBER_FORMATS["percentage"]
        }
    }


def create_date_format():
    """Create date format"""
    return {
        "numberFormat": {
            "type": "DATE",
            "pattern": NUMBER_FORMATS["date"]
        }
    }


def create_number_format(decimal_places=0):
    """Create whole number or decimal format"""
    if decimal_places > 0:
        pattern = f"#,##0.{'0' * decimal_places}"
    else:
        pattern = NUMBER_FORMATS["whole_number"]
    return {
        "numberFormat": {
            "type": "NUMBER",
            "pattern": pattern
        }
    }


def create_conditional_format_rule(sheet_id, start_row, end_row, start_col, end_col,
                                    condition_type, values, format_type="background"):
    """
    Create a conditional formatting rule

    condition_type: "NUMBER_GREATER", "NUMBER_LESS", "NUMBER_BETWEEN",
                   "TEXT_CONTAINS", "CUSTOM_FORMULA"
    format_type: "background", "text"
    """
    rule = {
        "ranges": [{
            "sheetId": sheet_id,
            "startRowIndex": start_row,
            "endRowIndex": end_row,
            "startColumnIndex": start_col,
            "endColumnIndex": end_col
        }],
        "booleanRule": {
            "condition": {
                "type": condition_type,
                "values": values
            },
            "format": {}
        }
    }
    return rule


def create_gradient_rule(sheet_id, start_row, end_row, start_col, end_col,
                         min_color, mid_color, max_color):
    """Create a gradient conditional formatting rule"""
    return {
        "ranges": [{
            "sheetId": sheet_id,
            "startRowIndex": start_row,
            "endRowIndex": end_row,
            "startColumnIndex": start_col,
            "endColumnIndex": end_col
        }],
        "gradientRule": {
            "minpoint": {
                "color": min_color,
                "type": "MIN"
            },
            "midpoint": {
                "color": mid_color,
                "type": "PERCENTILE",
                "value": "50"
            },
            "maxpoint": {
                "color": max_color,
                "type": "MAX"
            }
        }
    }


def get_color_rule(condition, format_color, is_background=True):
    """
    Helper to create color formatting based on condition

    condition examples:
    - {"type": "NUMBER_GREATER", "values": [{"userEnteredValue": "0"}]}
    - {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": "=A1>100"}]}
    """
    format_dict = {}
    if is_background:
        format_dict["backgroundColor"] = format_color
    else:
        format_dict["textFormat"] = {"foregroundColor": format_color}

    return {
        "booleanRule": {
            "condition": condition,
            "format": format_dict
        }
    }


def apply_standard_formatting(service, spreadsheet_id, sheet_id, num_rows, num_cols):
    """Apply standard formatting to a sheet"""
    requests = []

    # Freeze first row
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 1
                }
            },
            "fields": "gridProperties.frozenRowCount"
        }
    })

    # Format header row
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols
            },
            "cell": {
                "userEnteredFormat": create_header_format()
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    })

    # Set default font for data rows
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 1,
                "endRowIndex": num_rows,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols
            },
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {
                        "fontSize": 10,
                        "fontFamily": "Arial"
                    }
                }
            },
            "fields": "userEnteredFormat.textFormat"
        }
    })

    # Add auto-filter
    requests.append({
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": num_rows,
                    "startColumnIndex": 0,
                    "endColumnIndex": num_cols
                }
            }
        }
    })

    return requests


def create_income_expense_formatting(sheet_id, amount_col, start_row, end_row):
    """Create conditional formatting for income (green) and expenses (red)"""
    return [
        # Green for positive (income)
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": amount_col,
                        "endColumnIndex": amount_col + 1
                    }],
                    "booleanRule": {
                        "condition": {
                            "type": "NUMBER_GREATER",
                            "values": [{"userEnteredValue": "0"}]
                        },
                        "format": {
                            "textFormat": {"foregroundColor": COLORS["positive"]}
                        }
                    }
                },
                "index": 0
            }
        },
        # Red for negative (expenses)
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": amount_col,
                        "endColumnIndex": amount_col + 1
                    }],
                    "booleanRule": {
                        "condition": {
                            "type": "NUMBER_LESS",
                            "values": [{"userEnteredValue": "0"}]
                        },
                        "format": {
                            "textFormat": {"foregroundColor": COLORS["negative"]}
                        }
                    }
                },
                "index": 1
            }
        }
    ]


def create_budget_formatting(sheet_id, percent_col, start_row, end_row):
    """Create conditional formatting for budget percentage used"""
    rules = []
    thresholds = [
        (75, COLORS["positive"]),      # Green <75%
        (90, {"red": 0.95, "green": 0.76, "blue": 0.20}),  # Yellow 75-90%
        (100, COLORS["warning"]),      # Orange 90-100%
        (999, COLORS["negative"])      # Red >100%
    ]

    for i, (threshold, color) in enumerate(thresholds):
        if i == 0:
            condition = {
                "type": "NUMBER_LESS",
                "values": [{"userEnteredValue": str(threshold/100)}]
            }
        elif i == len(thresholds) - 1:
            condition = {
                "type": "NUMBER_GREATER_THAN_EQ",
                "values": [{"userEnteredValue": str(thresholds[i-1][0]/100)}]
            }
        else:
            condition = {
                "type": "NUMBER_BETWEEN",
                "values": [
                    {"userEnteredValue": str(thresholds[i-1][0]/100)},
                    {"userEnteredValue": str(threshold/100)}
                ]
            }

        rules.append({
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": percent_col,
                        "endColumnIndex": percent_col + 1
                    }],
                    "booleanRule": {
                        "condition": condition,
                        "format": {
                            "backgroundColor": color
                        }
                    }
                },
                "index": i
            }
        })

    return rules


def create_health_score_formatting(sheet_id, score_col, start_row, end_row,
                                    thresholds=None):
    """
    Create conditional formatting for health scores (Oura style)
    Default thresholds: Green >75, Yellow 60-75, Orange 45-60, Red <45
    """
    if thresholds is None:
        thresholds = [
            (45, COLORS["negative"]),                              # Red <45
            (60, COLORS["warning"]),                               # Orange 45-60
            (75, {"red": 0.95, "green": 0.76, "blue": 0.20}),     # Yellow 60-75
            (100, COLORS["positive"])                              # Green >75
        ]

    rules = []
    for i, (threshold, color) in enumerate(thresholds):
        if i == 0:
            condition = {
                "type": "NUMBER_LESS",
                "values": [{"userEnteredValue": str(threshold)}]
            }
        else:
            condition = {
                "type": "NUMBER_BETWEEN",
                "values": [
                    {"userEnteredValue": str(thresholds[i-1][0])},
                    {"userEnteredValue": str(threshold)}
                ]
            }

        rules.append({
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": score_col,
                        "endColumnIndex": score_col + 1
                    }],
                    "booleanRule": {
                        "condition": condition,
                        "format": {
                            "backgroundColor": color
                        }
                    }
                },
                "index": i
            }
        })

    return rules
