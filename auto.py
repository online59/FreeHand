import pyautogui
import numpy as np
import pyperclip
from time import sleep
from datetime import datetime
from dateutil.parser import parse

# Delay hotkey 100 milisec
INTERVAL = 0.1

# Send key to another program, The program will return False if there is error
def send_keys(key, field=None, value=None):
    
    # Lower key
    key = key.lower()

    # Request for pressing alt
    if key[0] == '%':
        pyautogui.hotkey('alt', key[1:])

    # Request to type text
    elif key == '$text':

	  # Check if the columns is empty
        if value == np.nan or value == 'nan' or value == np.NAN or value == '' or value == None:
            return False
        
        # If it was a date column, then format date first
        if field == 'วันที่' or field == 'วัน' or field.lower() == 'date':
		
            try:
                raw_date = parse(value.strip(' '))
            except:
                print('Error auto.py/34: Date format may not be correct')
                return False

            value = raw_date.strftime('%d/%m/%y')

        pyperclip.copy(value)
        
        try:
            with pyautogui.hold('ctrl'):
                sleep(INTERVAL)
                pyautogui.press('v')
        except:
            print('Error auto.py/46: Copy/paste shortcut not working')
            return False

        print(value)

    # press key
    else:

        try:
            pyautogui.press(key)
        except:
            print('Error auto.py/52: Key pressing function may not work properly')
            return False

    # If everything OK, continue
    return True