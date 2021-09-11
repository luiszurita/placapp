# PlacApp: this is an App that receives a car's license plate and checks
# if it should be currently transiting through Quito's streets according
# the 'Pico & Placa' law along with more useful information.
# by Luis Zurita

import pywebio
from pywebio.input import input, FLOAT, checkbox
from pywebio.output import put_text

def pipa():
    license = input("Enter the license plate number: ", type=FLOAT)#string
    c_date_time = checkbox(options=['use current date', 'use current time'])


if __name__ == '__main__':
    pywebio.start_server(pipa, port=80)
