import requests
from utils.login_polimi import good_cookies
import random
from datetime import datetime
from utils.colors import print_colored
from utils.set_time import get_time
from attendance.get_lesson import RetrieveLesson

def check_in():
    data = self.get_check_in_data()
    lat = data[0]
    long = data[1]
    checkin_id = data[2]

    body = "{\"id\":\"" + checkin_id + "\",\"type\":\"LS\",\"userLocation\":{\"longitude\":" + str(long) + ",\"latitude\":" + str(lat) + "}}"
    r = requests.post("https://www.gsom.polimi.it/api/student/checkin/", headers=self.header, data=body).json()

    if r['success']:
        print_colored(f'[ {get_time()} ] [ SUCCESSFULLY CHECKED-IN ]', 'green')
    elif str(r['data']['reason']) == '1':
        print_colored(f'[ {get_time()} ] [ CHECK-IN ALREADY VALIDATED ]', 'green')
    elif str(r['data']['reason']) == '2':
        print_colored(f'[ {get_time()} ] [ UNABLE TO CHECK-IN | GPS SPOOFING NOT WORKING ]', 'red')

