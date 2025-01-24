import requests
from utils.login_polimi import good_cookies
import random
from datetime import datetime
from utils.colors import print_colored
from utils.set_time import get_time


class RetrieveLesson:
    def __init__(self):
        data = good_cookies()
        self.cookie = data[0]
        self.pid = 'abc6fbc8-3198-ee11-be37-0022489cecab'
        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/73.0.3683.103 Safari/537.36'
        ]

        self.header = {
            "User-Agent": random.choice(user_agent_list),
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7",
            "client": "desktop",
            "client-version": "3.132.0",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": self.cookie
        }

    def get_check_in_data(self):
        r = requests.get(f'https://www.gsom.polimi.it/api/programs/getProgramCalenderEvents/?id={self.pid}',
                         headers=self.header).json()
        data = r['data']

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
                print_colored(f"[ {get_time()} ] [ LESSON FOUND! ]", 'yellow')

                lat = item['building']['latitude']
                long = item['building']['longitude']
                checkin_id = item['id']
                return [lat, long, checkin_id]
            continue
