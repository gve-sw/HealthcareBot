from datetime import datetime

my_date="04/07/2019 08:00:00 p.m.".replace('.','')

print(my_date)
datetime_object = datetime.strptime(my_date, '%d/%m/%Y %I:%M:%S %p')
print(datetime_object)

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