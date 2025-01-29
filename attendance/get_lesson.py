import requests
from datetime import datetime
from utils.colors import print_colored
from utils.set_time import get_time
from utils.comp_headers import woof


class RetrieveLesson:
    def __init__(self, pid, header):
        self.pid = pid
        self.header = header

    def get_check_in_data(self):
        r = requests.get(f'https://www.gsom.polimi.it/api/programs/getProgramCalenderEvents/?id={self.pid}',
                         headers=self.header).json()
        data = r['data']
        i = 0

        for item in data:
            start = item['startDate']
            end = item['endDate']
            try:
                start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
                end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
            except TypeError:
                continue
            current_time = datetime.utcnow()

            if start_dt <= current_time <= end_dt:
                i += 1
                print_colored(f"[ {get_time()} ] [ LESSON FOUND! ]", 'yellow')

                lat = item['building']['latitude']
                long = item['building']['longitude']
                checkin_id = item['id']
                return [lat, long, checkin_id, self.header]
            continue
        if i == 0:
            print_colored(f"[ {get_time()} ] [ NO LESSON FOUND ]\n", 'yellow')
            return []
