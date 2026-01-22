"""
Data validation utilities for Life OS v2 Google Sheets
"""


def create_dropdown_validation(sheet_id, start_row, end_row, start_col, end_col, values):
    """
    Create dropdown data validation rule

    values: list of strings for dropdown options
    """
    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": v} for v in values]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    }


def create_dropdown_from_range(sheet_id, start_row, end_row, start_col, end_col, source_range):
    """
    Create dropdown data validation from another range

    source_range: e.g., "'Categories'!A:A"
    """
    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_RANGE",
                    "values": [{"userEnteredValue": f"={source_range}"}]
                },
                "showCustomUi": True,
                "strict": False
            }
        }
    }


def create_checkbox_validation(sheet_id, start_row, end_row, start_col, end_col,
                                checked_value="TRUE", unchecked_value="FALSE"):
    """Create checkbox data validation"""
    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": {
                    "type": "BOOLEAN"
                }
            }
        }
    }


def create_date_validation(sheet_id, start_row, end_row, start_col, end_col,
                           min_date=None, max_date=None):
    """Create date validation rule"""
    condition = {"type": "DATE_IS_VALID"}

    if min_date and max_date:
        condition = {
            "type": "DATE_BETWEEN",
            "values": [
                {"userEnteredValue": min_date},
                {"userEnteredValue": max_date}
            ]
        }
    elif min_date:
        condition = {
            "type": "DATE_ON_OR_AFTER",
            "values": [{"userEnteredValue": min_date}]
        }
    elif max_date:
        condition = {
            "type": "DATE_ON_OR_BEFORE",
            "values": [{"userEnteredValue": max_date}]
        }

    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": condition,
                "strict": True
            }
        }
    }


def create_number_validation(sheet_id, start_row, end_row, start_col, end_col,
                              min_value=None, max_value=None, allow_decimal=True):
    """Create number validation rule"""
    if min_value is not None and max_value is not None:
        condition = {
            "type": "NUMBER_BETWEEN",
            "values": [
                {"userEnteredValue": str(min_value)},
                {"userEnteredValue": str(max_value)}
            ]
        }
    elif min_value is not None:
        condition = {
            "type": "NUMBER_GREATER_THAN_EQ",
            "values": [{"userEnteredValue": str(min_value)}]
        }
    elif max_value is not None:
        condition = {
            "type": "NUMBER_LESS_THAN_EQ",
            "values": [{"userEnteredValue": str(max_value)}]
        }
    else:
        condition = {"type": "NUMBER_GREATER_THAN", "values": [{"userEnteredValue": "-99999999"}]}

    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": condition,
                "strict": True
            }
        }
    }


def create_text_validation(sheet_id, start_row, end_row, start_col, end_col,
                           contains=None, not_contains=None, is_email=False, is_url=False):
    """Create text validation rule"""
    if is_email:
        condition = {"type": "TEXT_IS_EMAIL"}
    elif is_url:
        condition = {"type": "TEXT_IS_URL"}
    elif contains:
        condition = {
            "type": "TEXT_CONTAINS",
            "values": [{"userEnteredValue": contains}]
        }
    elif not_contains:
        condition = {
            "type": "TEXT_NOT_CONTAINS",
            "values": [{"userEnteredValue": not_contains}]
        }
    else:
        condition = {"type": "TEXT_NOT_EQ", "values": [{"userEnteredValue": ""}]}

    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": condition,
                "strict": False
            }
        }
    }


def create_custom_formula_validation(sheet_id, start_row, end_row, start_col, end_col,
                                      formula, error_message=None):
    """
    Create custom formula validation

    formula: e.g., "=A1>0" or "=AND(A1>=0,A1<=100)"
    """
    rule = {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "rule": {
                "condition": {
                    "type": "CUSTOM_FORMULA",
                    "values": [{"userEnteredValue": formula}]
                },
                "strict": True
            }
        }
    }

    if error_message:
        rule["setDataValidation"]["rule"]["inputMessage"] = error_message

    return rule


def remove_validation(sheet_id, start_row, end_row, start_col, end_col):
    """Remove data validation from a range"""
    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            }
        }
    }


# Predefined validation rules for common use cases
def create_priority_validation(sheet_id, start_row, end_row, col):
    """Create priority dropdown (P0-P3)"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["priority"]
    )


def create_status_validation(sheet_id, start_row, end_row, col):
    """Create status dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["status"]
    )


def create_owner_validation(sheet_id, start_row, end_row, col):
    """Create owner dropdown (Michelle/Gray/Both)"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["task_owner"]
    )


def create_goal_category_validation(sheet_id, start_row, end_row, col):
    """Create goal category dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["goal_category"]
    )


def create_goal_status_validation(sheet_id, start_row, end_row, col):
    """Create goal status dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["goal_status"]
    )


def create_frequency_validation(sheet_id, start_row, end_row, col):
    """Create frequency dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["frequency"]
    )


def create_cervical_mucus_validation(sheet_id, start_row, end_row, col):
    """Create cervical mucus dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["cervical_mucus"]
    )


def create_cycle_phase_validation(sheet_id, start_row, end_row, col):
    """Create cycle phase dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["cycle_phase"]
    )


def create_job_stage_validation(sheet_id, start_row, end_row, col):
    """Create job stage dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["job_stage"]
    )


def create_location_type_validation(sheet_id, start_row, end_row, col):
    """Create location type dropdown (Remote/Hybrid/On-site)"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["location_type"]
    )


def create_sales_channel_validation(sheet_id, start_row, end_row, col):
    """Create sales channel dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["sales_channel"]
    )


def create_customer_type_validation(sheet_id, start_row, end_row, col):
    """Create customer type dropdown"""
    from config.settings import VALIDATION
    return create_dropdown_validation(
        sheet_id, start_row, end_row, col, col + 1,
        VALIDATION["customer_type"]
    )


def create_score_validation(sheet_id, start_row, end_row, col, min_val=0, max_val=100):
    """Create score validation (0-100 by default)"""
    return create_number_validation(
        sheet_id, start_row, end_row, col, col + 1,
        min_value=min_val, max_value=max_val
    )


def create_rating_validation(sheet_id, start_row, end_row, col, max_rating=10):
    """Create rating validation (1-10 by default)"""
    return create_number_validation(
        sheet_id, start_row, end_row, col, col + 1,
        min_value=1, max_value=max_rating
    )
