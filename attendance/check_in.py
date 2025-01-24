import requests
from utils.colors import print_colored
from utils.set_time import get_time
from attendance.get_lesson import RetrieveLesson
from utils.comp_headers import woof


def check_in():
    check_data = RetrieveLesson().get_check_in_data()

    body = "{\"id\":\"" + check_data[2] + "\",\"type\":\"LS\",\"userLocation\":{\"longitude\":" + str(check_data[1]) + ",\"latitude\":" + str(check_data[0]) + "}}"
    r = requests.post("https://www.gsom.polimi.it/api/student/checkin/", headers=check_data[3], data=body).json()
    # fix checks

    if r['success']:
        print_colored(f'[ {get_time()} ] [ SUCCESSFULLY CHECKED-IN ]', 'green')
    elif str(r['data']['reason']) == '1':
        print_colored(f'[ {get_time()} ] [ CHECK-IN ALREADY VALIDATED ]', 'green')
    elif str(r['data']['reason']) == '2':
        print_colored(f'[ {get_time()} ] [ UNABLE TO CHECK-IN | GPS SPOOFING NOT WORKING ]', 'red')

