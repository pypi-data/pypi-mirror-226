
from datetime import datetime, timedelta

dateformat = getattr('DATEFORMAT', '%Y-%m-%d')

def validate_date(date_text):
        try:
            datetime.strptime(date_text, dateformat)
            return True
        except ValueError:
            return False

def future_validate_date(date):
    if date > datetime.now().date():
        return "Date cannot be in the past"

def count_days_from_today(date):
    if validate_date(date) == True:
        try:
            today = datetime.now()
            selecteddate = datetime.strptime(date, dateformat)
            return (selecteddate-today).days
        except:
            return False
        

def get_week_list_for_date(date):
    list = []
    for i in reversed(range(0,3)):
        ddate =((datetime.strptime(date, dateformat) - timedelta(days=i)))
        if count_days_from_today(ddate.strftime(dateformat)) >= -1:
           list.append(ddate)
    for i in range(1,3):
        ddate =((datetime.strptime(date, dateformat) + timedelta(days=i)))
        if count_days_from_today(ddate.strftime(dateformat)) >= 0:
           list.append(ddate)
    return(list)