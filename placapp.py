# PlacApp: this is an App that receives a car's license plate and checks
# if it should be currently transiting through Quito's streets according
# the 'Pico & Placa' law along with more useful information.
# by Luis Zurita

import pywebio #requires: tornado and user-agents
import datetime
from pywebio.input import input, checkbox, TEXT, DATE, TIME
from pywebio.output import put_text

def pipa():
    license = input("Enter the license plate number: ",placeholder="AAA-000(0)"
                                                      ,required=True)
    c_date_time = checkbox(options=['use current date', 'use current time'],
                           help_text='The fields not chosen will then be entered manually')
    if 'use current date' not in c_date_time:
        my_date = input("Enter date (dd/mm/yyyy): ", type=DATE, required=True)
        my_date = datetime.datetime.strptime(my_date, "%Y-%m-%d").date()
        weekday = my_date.strftime('%A')
    # else:

    if 'use current time' not in c_date_time:
        my_time = input("Enter time (23:59): ", type=TIME, required=True)

    print(my_date)
    print(weekday)
    print(my_time)

if __name__ == '__main__':
    pywebio.start_server(pipa, port=80)
