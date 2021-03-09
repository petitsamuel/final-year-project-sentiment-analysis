import datetime

format = "%Y-%m-d"

def is_valid_date_format(str_value):
    try:
        datetime.datetime.strptime(str_value, format)
        return True
    except ValueError:
        # Date not in yyyy-mm-dd format
        return False
