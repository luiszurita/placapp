# PlacApp: this is an App that receives a car's license plate and checks
# if it should be currently transiting through Quito's streets according
# the 'Pico & Placa' law along with more useful information.
# by Luis Zurita

import pywebio #requires: tornado and user-agents
import datetime
import re
from pywebio.input import input, checkbox, TEXT, DATE, TIME
from pywebio.output import put_text

def pipa():
    def check_plate(lic):
        matched = bool(re.match(r'[a-zA-Z]{3}-[0-9]{3,4}$',str(lic)))
        if matched == False:
            return 'input does not match expected format'

    license = input("Enter the license plate number: ",placeholder="AAA-000(0)"
                                                      ,required=True
                                                      ,validate=check_plate)

    last_digit = str(license)[-1]

    c_date_time = checkbox(options=['use current date', 'use current time'],
                           help_text='The fields not chosen will then be entered manually')
    if 'use current date' not in c_date_time:
        my_date = input("Select date (dd/mm/yyyy): ", type=DATE, required=True)
        my_date = datetime.datetime.strptime(my_date, "%Y-%m-%d").date()
        weekday = my_date.strftime('%A')
    else:
        today = datetime.date.today()
        my_date = datetime.datetime.strptime(str(today), "%Y-%m-%d").date()
        weekday = my_date.strftime('%A')

    if 'use current time' not in c_date_time:
        my_time = input("Enter time (23:59): ", type=TIME, required=True)
    else:
        my_time = datetime.datetime.now().strftime("%H:%M")

    day_plates = {'Monday':(1,2),'Tuesday':(3,4),
                  'Wednesday':(5,6),'Thursday':(7,8),
                  'Friday':(9,0)}

    b1 = datetime.datetime.now().replace(hour=7, minute=0).strftime("%H:%M")
    print(b1)

    # if weekday in day_plates.keys():
    #     if last_digit in day_plates[weekday]:
    #         if (my_time > my)

    #TODO find way to compare time to raise flags
    # add input for previous sanctions to calculate fine ammount
    
    print(my_date)
    print(weekday)
    print(my_time)

if __name__ == '__main__':
    pywebio.start_server(pipa, port=80)
