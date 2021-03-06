# PlacApp: this is an App that receives a car's license plate and checks
# if it should be currently transiting through Quito's streets according
# the 'Pico & Placa' law along with more useful information.
# for this app to be executed locally we need: 'pywebio', 'user-agents',
# and 'tornado' in our environment
# the app will run on localhost:80
# by Luis Zurita

import pywebio #requires: tornado and user-agents
import datetime
import re
from pywebio.input import input, checkbox, select, DATE, TIME
from pywebio.output import put_text, put_markdown, put_table, put_html

def pipa():
    # validation function for input plate
    def check_plate(lic):
        matched = bool(re.match(r'[a-zA-Z]{3}-[0-9]{3,4}$',str(lic)))
        if matched == False:
            return 'input does not match expected format'

    license = input("Enter the license plate number: ",placeholder="AAA-000(0)"
                                                      ,required=True
                                                      ,validate=check_plate)

    last_digit = int(str(license)[-1])

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

    prev_fines = select(label='Enter number of previous Pico&Placa fines',
                        options=['0', '1', '2+'],
                        help_text='must select one option')
    fines_dict = {1:57.90,2:96.50,3:193}
    if prev_fines == '0':
        next_fine = fines_dict[1]
    elif prev_fines == '1':
        next_fine = fines_dict[2]
    elif prev_fines == '2+':
        next_fine = fines_dict[3]

    day_plates = {'Monday':(1,2),'Tuesday':(3,4),
                  'Wednesday':(5,6),'Thursday':(7,8),
                  'Friday':(9,0)}

    for days in day_plates.values():
        if last_digit in days:
            no_transit_day = list(day_plates.keys())[list(day_plates.values()).index(days)]
    #pico and placa times
    b1 = datetime.datetime.now().replace(hour=7, minute=0).strftime("%H:%M")
    e1 = datetime.datetime.now().replace(hour=9, minute=30).strftime("%H:%M")
    b2 = datetime.datetime.now().replace(hour=16, minute=0).strftime("%H:%M")
    e2 = datetime.datetime.now().replace(hour=19, minute=30).strftime("%H:%M")

    # time_compare method compares two time strings and returns:
    # 0 if the first input is the greatest
    # 1 if the inputs are equal
    # 2 if the second input is the greatest
    def time_compare(t1,t2):
        t1_h, t1_m = t1.split(':')
        t2_h, t2_m = t2.split(':')
        if int(t1_h) > int(t2_h):
            return 0
        elif int(t1_h) == int(t2_h):
            if int(t1_m) > int(t2_m):
                return 0
            elif int(t1_m) == int(t2_m):
                return 1
            elif int(t1_m) < int(t2_m):
                return 2
        elif int(t1_h) < int(t2_h):
            return 2

    should_transit = None

    if weekday in day_plates.keys():
        if last_digit in day_plates[weekday]:
            if time_compare(my_time,b1) <= 1 and time_compare(my_time,e1) >= 1:
                should_transit = False
            elif time_compare(my_time,b2) <= 1 and time_compare(my_time,e2) >= 1:
                should_transit = False
            else:
                should_transit = True
        else:
            should_transit = True
    else:
        should_transit = True

    if should_transit == False:
        put_markdown('# **The vehicle with the plate %s should NOT be transiting on %s at %s**'%(license,my_date,my_time))
        put_html('<hr>')
        put_table([
                  ["Vehicle's Licese Plate",'Last Digit','No Transit Day','Amount of possible fine'],
                  [license, last_digit, no_transit_day,'$%s'%(next_fine)]
        ])
    else:
        put_markdown('# **The vehicle with the plate %s is OK to be transiting on %s at %s**'%(license,my_date,my_time))
        put_html('<hr>')
        put_table([
                  ["Vehicle's Licese Plate",'Last Digit','No Transit Day'],
                  [license, last_digit, no_transit_day]
        ])

    print('Search done')

if __name__ == '__main__':
    pywebio.start_server(pipa, port=80)
