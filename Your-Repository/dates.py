#import datetime add datetime and datetime we can to get time(now)
import datetime

x = datetime.datetime.now()
print(x)

x = datetime.datetime.now()

print(x.year) # we can to get year
print(x.strftime("%A"))  #here strftime it's make orderly and &A it's full day of the week

import datetime

x = datetime.datetime(2007, 9, 17) #Here we to get year, month and day, hour, minut, second no
#because we did't give.

print(x)