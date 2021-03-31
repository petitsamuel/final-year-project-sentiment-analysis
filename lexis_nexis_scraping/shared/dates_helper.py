from datetime import datetime

def date_from_week(week, year):
    return datetime.strptime("%d%d0" % (year, week), '%Y%W%w')

def date_from_month(month, year):
   return datetime.strptime("%d-%d" % (year, month), '%Y-%m')