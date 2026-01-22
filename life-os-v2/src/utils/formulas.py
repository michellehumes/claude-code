"""
Formula generators for Life OS v2 Google Sheets
"""


def sumif_formula(range_ref, criteria, sum_range):
    """
    Generate SUMIF formula

    Example: =SUMIF(Transactions!C:C,"Groceries",Transactions!G:G)
    """
    return f'=SUMIF({range_ref},"{criteria}",{sum_range})'


def sumifs_formula(sum_range, *criteria_pairs):
    """
    Generate SUMIFS formula

    Example: =SUMIFS(Transactions!G:G,Transactions!C:C,"Groceries",Transactions!A:A,">=1/1/2026")
    criteria_pairs: list of (range, criteria) tuples
    """
    criteria_str = ",".join([f'{r},"{c}"' for r, c in criteria_pairs])
    return f'=SUMIFS({sum_range},{criteria_str})'


def countif_formula(range_ref, criteria):
    """
    Generate COUNTIF formula

    Example: =COUNTIF(Transactions!C:C,"Groceries")
    """
    return f'=COUNTIF({range_ref},"{criteria}")'


def countifs_formula(*criteria_pairs):
    """
    Generate COUNTIFS formula

    criteria_pairs: list of (range, criteria) tuples
    """
    criteria_str = ",".join([f'{r},"{c}"' for r, c in criteria_pairs])
    return f'=COUNTIFS({criteria_str})'


def averageif_formula(range_ref, criteria, avg_range):
    """
    Generate AVERAGEIF formula

    Example: =AVERAGEIF(Transactions!C:C,"Groceries",Transactions!G:G)
    """
    return f'=AVERAGEIF({range_ref},"{criteria}",{avg_range})'


def vlookup_formula(lookup_value, table_range, col_index, is_sorted=False):
    """
    Generate VLOOKUP formula

    Example: =VLOOKUP(A2,'Job Pipeline'!A:Z,5,FALSE)
    """
    sorted_str = "TRUE" if is_sorted else "FALSE"
    return f'=VLOOKUP({lookup_value},{table_range},{col_index},{sorted_str})'


def if_formula(condition, true_value, false_value):
    """
    Generate IF formula

    Example: =IF(A1>0,"Income","Expense")
    """
    return f'=IF({condition},{true_value},{false_value})'


def ifs_formula(*condition_value_pairs):
    """
    Generate IFS formula

    condition_value_pairs: list of (condition, value) tuples
    """
    pairs_str = ",".join([f'{c},{v}' for c, v in condition_value_pairs])
    return f'=IFS({pairs_str})'


def today_formula():
    """Generate TODAY() formula"""
    return "=TODAY()"


def now_formula():
    """Generate NOW() formula"""
    return "=NOW()"


def sparkline_formula(data_range, chart_type="line", options=None):
    """
    Generate SPARKLINE formula

    chart_type: "line", "bar", "column", "winloss"
    options: dict of sparkline options
    """
    if options:
        opts_str = ",".join([f'"{k}",{v}' for k, v in options.items()])
        return f'=SPARKLINE({data_range},{{{opts_str}}})'
    return f'=SPARKLINE({data_range})'


def date_diff_formula(start_date, end_date, unit="D"):
    """
    Generate DATEDIF formula

    unit: "D" (days), "M" (months), "Y" (years)
    """
    return f'=DATEDIF({start_date},{end_date},"{unit}")'


def text_formula(value, format_str):
    """
    Generate TEXT formula

    Example: =TEXT(A1,"$#,##0.00")
    """
    return f'=TEXT({value},"{format_str}")'


def concat_formula(*values):
    """Generate CONCATENATE formula"""
    return f'=CONCATENATE({",".join(values)})'


def query_formula(data_range, query_str, headers=1):
    """
    Generate QUERY formula

    Example: =QUERY(Transactions!A:I,"SELECT A,G WHERE C='Groceries'",1)
    """
    return f'=QUERY({data_range},"{query_str}",{headers})'


def unique_formula(range_ref):
    """Generate UNIQUE formula"""
    return f'=UNIQUE({range_ref})'


def filter_formula(range_ref, condition):
    """
    Generate FILTER formula

    Example: =FILTER(A:B,C:C="Active")
    """
    return f'=FILTER({range_ref},{condition})'


def sort_formula(range_ref, sort_col, ascending=True):
    """Generate SORT formula"""
    order = "TRUE" if ascending else "FALSE"
    return f'=SORT({range_ref},{sort_col},{order})'


def index_match_formula(return_range, lookup_range, lookup_value, match_type=0):
    """
    Generate INDEX/MATCH formula

    Example: =INDEX(B:B,MATCH(A1,A:A,0))
    """
    return f'=INDEX({return_range},MATCH({lookup_value},{lookup_range},{match_type}))'


def sumproduct_formula(*arrays):
    """Generate SUMPRODUCT formula"""
    return f'=SUMPRODUCT({",".join(arrays)})'


def eomonth_formula(start_date, months=0):
    """Generate EOMONTH formula (end of month)"""
    return f'=EOMONTH({start_date},{months})'


def month_start_formula(date_ref):
    """Generate formula for start of month"""
    return f'=DATE(YEAR({date_ref}),MONTH({date_ref}),1)'


def days_since_formula(date_ref):
    """Generate formula for days since a date"""
    return f'=TODAY()-{date_ref}'


def percentage_formula(numerator, denominator):
    """Generate percentage formula with error handling"""
    return f'=IFERROR({numerator}/{denominator},0)'


def running_total_formula(sum_range, current_row):
    """Generate running total formula"""
    return f'=SUM($G$2:G{current_row})'


def ytd_sum_formula(date_col, amount_col, criteria_col=None, criteria=None):
    """Generate Year-to-Date sum formula"""
    if criteria_col and criteria:
        return f'=SUMIFS({amount_col},{date_col},">=1/1/"&YEAR(TODAY()),{date_col},"<="&TODAY(),{criteria_col},"{criteria}")'
    return f'=SUMIFS({amount_col},{date_col},">=1/1/"&YEAR(TODAY()),{date_col},"<="&TODAY())'


def mtd_sum_formula(date_col, amount_col, criteria_col=None, criteria=None):
    """Generate Month-to-Date sum formula"""
    if criteria_col and criteria:
        return f'=SUMIFS({amount_col},{date_col},">=DATE(YEAR(TODAY()),MONTH(TODAY()),1)",{date_col},"<="&TODAY(),{criteria_col},"{criteria}")'
    return f'=SUMIFS({amount_col},{date_col},">=DATE(YEAR(TODAY()),MONTH(TODAY()),1)",{date_col},"<="&TODAY())'


def moving_average_formula(range_ref, periods=7):
    """Generate moving average formula"""
    return f'=AVERAGE(OFFSET({range_ref},-{periods-1},0,{periods},1))'


def trend_indicator_formula(current, previous):
    """Generate trend indicator formula (↑↓→)"""
    return f'=IF({current}>{previous},"↑",IF({current}<{previous},"↓","→"))'


def health_status_formula(score, thresholds=None):
    """
    Generate health status formula based on score

    Default: Optimal (>85), Good (70-85), Pay Attention (55-70), Rest (<55)
    """
    if thresholds is None:
        thresholds = [85, 70, 55]
    return f'=IF({score}>={thresholds[0]},"🟢 Optimal",IF({score}>={thresholds[1]},"🟡 Good",IF({score}>={thresholds[2]},"🟠 Pay Attention","🔴 Rest Needed")))'


def cycle_day_formula(current_date, cycle_start):
    """Generate cycle day calculation formula"""
    return f'={current_date}-{cycle_start}+1'


def ovulation_estimate_formula(cycle_start):
    """Generate estimated ovulation date formula (cycle start + 14 days)"""
    return f'={cycle_start}+14'


def luteal_phase_formula(cycle_length, ovulation_day):
    """Generate luteal phase length formula"""
    return f'={cycle_length}-{ovulation_day}'


def dpo_formula(current_date, ovulation_date):
    """Generate Days Past Ovulation formula"""
    return f'=IF({ovulation_date}="","",{current_date}-{ovulation_date})'


def bbt_shift_formula(current_temp, baseline_temp, threshold=0.2):
    """Generate BBT temperature shift detection formula"""
    return f'=IF({current_temp}-{baseline_temp}>={threshold},"Y","N")'
