import requests
from utils.colors import print_colored
from utils.set_time import get_time
from attendance.get_lesson import RetrieveLesson
from utils.comp_headers import woof


def check_out(pid, header):
    check_data = RetrieveLesson(pid, header).get_check_in_data()
    if len(check_data) == 0:
        return
    print_colored(f'[ {get_time()} ] [ CHECKING OUT... ]', 'yellow')

    body = "{\"id\":\"" + str(check_data[2]) + "\",\"type\":\"LS\",\"userLocation\":{\"longitude\":" + str(check_data[1]) + ",\"latitude\":" + str(check_data[0]) + "}}"
    r = requests.post("https://www.gsom.polimi.it/api/programs/checkout/", headers=check_data[3], data=body)

    if r.status_code == 204:
        print_colored(f'[ {get_time()} ] [ SUCCESSFULLY CHECKED-OUT ]\n', 'green')
    elif str(r.json()['data']['reason']) == '1':
        print_colored(f'[ {get_time()} ] [ CHECK-OUT ALREADY VALIDATED ]\n', 'green')
    elif str(r.json()['data']['reason']) == '2':
        print_colored(f'[ {get_time()} ] [ UNABLE TO CHECK-OUT | GPS SPOOFING NOT WORKING ]\n', 'red')
