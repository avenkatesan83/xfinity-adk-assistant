import datetime

def get_billing_info(account_id, month):
    """
    Returns mock billing information for the given account_id and month.
    month: int (1-12)
    """
    today = datetime.date.today()
    year = today.year

    # Get start and end date for the given month
    billing_start_date = datetime.date(year, month, 1)
    # Calculate last day of the month
    if month == 12:
        billing_end_date = datetime.date(year, month, 31)
    else:
        billing_end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    due_amount = "$ 150.75"  # Mock amount
    due_date = billing_end_date + datetime.timedelta(days=10)

    def format_date(dt):
        return dt.strftime("%m-%d-%Y")

    billing_info = {
        "account_id": account_id,
        "billing_start_date": format_date(billing_start_date),
        "billing_end_date": format_date(billing_end_date),
        "due_amount": due_amount,
        "due_date": format_date(due_date)
    }
    return billing_info