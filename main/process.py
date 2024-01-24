import datetime as dt
from .models import *
from django.contrib.auth.models import User
import calendar
from calendar import HTMLCalendar
from datetime import datetime



fname = open("logs.txt", "a")
print(fname)
def run_process(username ,  month = datetime.now().strftime('%B')):
       user = User.objects.get(username=username)
       print("----------------------",user)
       month_name =  month
       month_name = month_name.capitalize()  # Ensure the input is in title case
       l = list(calendar.month_name).index(month_name)
       trans = Transition.objects.filter(user = user , Transition_date__month = l-1 )
       for t in trans:
              print(t.category,"--------------",t.amount)

          



    # print(f"Processing at - {dt.datetime.now()}")
    # print("-------------..................>",User.id)
    # tr = Transition.objects.all()
    # # for t in tr:
    # #   print("----------->",User.id,t.category)
    # fname.write(f"Processing at - {dt.datetime.now()},\n")

