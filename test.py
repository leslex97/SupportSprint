import pytz # $ pip install pytz
x = pytz.all_timezones_set
for i in x:
    if i.startswith("Europe/W"):
        print(i)