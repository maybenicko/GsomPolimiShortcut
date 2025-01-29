import requests
from utils.colors import print_colored
from utils.set_time import get_time
from utils.comp_headers import woof
import json


class SendFeedback:
    def __init__(self, header):
        self.headers = header
        self.req_list = []

    def get_feedbacks(self):
        print_colored(f'[ {get_time()} ] [ GETTING FEEDBACK FORMS ]', 'yellow')
        r = requests.get('https://www.gsom.polimi.it/api/programs/feedbacks/', headers=self.headers).json()
        if len(r['data']) == 0:
            print_colored(f'[ {get_time()} ] [ NO FEEDBACK TO SEND ]\n', 'green')
            return False

        for feedback in r['data'][0]['courses']:
            lessons = feedback['lessons']

            for lesson in lessons:
                lesson_id = lesson['id']
                teacher_id = lesson['teachers'][0]['contactId']
                build = {
                    "lessonId": lesson_id,
                    "feedbacks": [
                        {
                            "teacherId": teacher_id,
                            "rating": "5",
                            "comment": ""
                        }
                    ]
                }
                self.req_list.append(build)
        return True

    def send_feedbacks(self):
        body = json.dumps(self.req_list)
        r = requests.post("https://www.gsom.polimi.it/api/programs/feedbacks/", headers=self.headers, data=body)

        if r.status_code == 204:
            print_colored(f'[ {get_time()} ] [ SUCCESSFULLY SENT {len(self.req_list)} FEEDBACKS! ]\n', 'green')
            return
        print_colored(f'[ {get_time()} ] [ ERROR SUBMITTING FEEDBACKS ] [ {r.status_code} ]\n', 'red')
        return

    def main(self):
        if not self.get_feedbacks():
            return
        self.send_feedbacks()
