from datetime import datetime, date

data = 'Sun, 26 May 2019 00:00:00 GMT'

eae = date.strftime(datetime.strptime( data , '%a, %d %B %Y 00:00:00 GMT'), '%d/%m/%y')

print(eae)