#from datetime import datetime

import re,datetime

s = "I have a meeting on 2018-12-10 in New York"
match = re.search('\d{4}-\d{2}-\d{2}', s)
print(match.group())
print(type(match.group()))
date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
print(date)


"""
my_date="04/07/2019 08:00:00 p.m.".replace('.','')

print(my_date)
datetime_object = datetime.strptime(my_date, '%d/%m/%Y %I:%M:%S %p')
print(datetime_object)
"""
"""
dict={
        'decade': '1970s',
        'artist': 'Debby Boone',
        'song': 'You Light Up My Life',
        'weeksAtOne': 10
    }

if 'decassde' in dict :
	print('hola')
"""