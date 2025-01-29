from add_calendar.g_cal import GoogleCalendarManager
from utils.colors import print_colored
from attendance.get_lesson import RetrieveLesson
from attendance.check_in import check_in
from attendance.check_out import check_out
from attendance.feedback import SendFeedback
from utils.comp_headers import woof


class UI:
    def __init__(self):
        self.main_menu = '[0] Quit.\n[1] Add lectures to your Google add_calendar. ' \
                         '(credentials.json needs to be updated with your Oauth) | NOT WORKING' \
                         '\n[2] Check-in\n[3] Check-out\n[4] Send Feedbacks'
        self.email = ''
        self.psw = ''
        self.data = []
        self.headers = ''
        self.pid = ''

    def get_session(self):
        self.data = woof(self.email, self.psw)
        self.headers = self.data[0]
        self.pid = self.data[1]

    def main(self):
        run = True
        while run:
            # add header handling so that the login is not called every single time
            print_colored(self.main_menu, 'blue')
            print_colored('Input your selection:', 'blue')
            selection = input('')

            if not selection.isdigit():
                print_colored('Wrong input, retry by selecting a number.', 'red')
                continue

            if self.email == '':
                print_colored('Input your email:', 'blue')
                self.email = input('')

            if self.psw == '':
                print_colored('Input your password:', 'blue')
                self.psw = input('')

            if len(self.data) == 0:
                self.get_session()

            if int(selection) == 0:
                run = False
                continue

            # not working
            elif int(selection) == 1:
                GoogleCalendarManager(self.email, self.psw).main()
                continue

            if int(selection) == 2 or int(selection) == 3:

                if int(selection) == 2:
                    check_in(self.pid, self.headers)
                    continue

                elif int(selection) == 3:
                    check_out(self.pid, self.headers)
                    continue

            if int(selection) == 4:
                SendFeedback(self.headers).main()
                continue

            print_colored('Unidentified error', 'red')


bot = UI()
bot.main()
