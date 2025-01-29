from add_calendar.g_cal import GoogleCalendarManager
from utils.colors import print_colored
from attendance.get_lesson import RetrieveLesson
from attendance.check_in import check_in
from attendance.check_out import check_out
from attendance.feedback import SendFeedback


class UI:
    def __init__(self):
        self.main_menu = '[0] Quit.\n[1] Add lectures to your Google add_calendar. ' \
                         '(credentials.json needs to be updated with your Oauth)' \
                         '\n[2] Check-in\n[3] Check-out\n[4] Send Feedbacks'
        self.email = ''
        self.psw = ''

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

            if int(selection) == 0:
                run = False
                continue

            elif int(selection) == 1:
                GoogleCalendarManager(self.email, self.psw).main()
                continue

            if int(selection) == 2 or int(selection) == 3:

                if int(selection) == 2:
                    check_in(self.email, self.psw)
                    continue

                elif int(selection) == 3:
                    check_out(self.email, self.psw)
                    continue

            if int(selection) == 4:
                SendFeedback(self.email, self.psw).main()
                continue

            print_colored('Unidentified error', 'red')


bot = UI()
bot.main()
