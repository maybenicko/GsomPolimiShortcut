from add_calendar.g_cal import GoogleCalendarManager
from utils.colors import print_colored
from attendance.get_lesson import RetrieveLesson
from attendance.check_in import check_in
from attendance.check_out import check_out


class UI:
    def __init__(self):
        self.main_menu = '[0] Quit.\n[1] Add lectures to your Google add_calendar. ' \
                         '(credentials.json needs to be updated with your Oauth)' \
                         '\n[2] Check-in\n[3] Check-out'
        self.campus_menu = '[0] Quit.\n[1] Campus Navigli\n[2] Campus Bovisa'

        # navigli gps
        self.navigli_long = '9.1675544'
        self.navigli_lat = '45.4502977'

        # bovisa gps
        self.bovisa_long = '9.1560426'
        self.bovisa_lat = '45.5034123'

        # to use
        self.lat = ''
        self.long = ''

    def campus_selection(self):
        run = True
        while run:
            print_colored(self.campus_menu, 'yellow')
            print_colored('Input your selection:', 'blue')
            campus = input('')

            if not campus.isdigit():
                print_colored('Wrong input, retry by selecting a number.', 'red')
                continue

            if int(campus) == 0:
                return 0

            elif int(campus) == 1:
                self.lat = self.navigli_lat
                self.long = self.navigli_long
                return 1

            elif int(campus) == 2:
                self.lat = self.bovisa_lat
                self.long = self.bovisa_long
                return 2

            print_colored('Wrong input, retry by selecting a number.', 'red')
            continue

    def main(self):
        run = True
        while run:
            print_colored(self.main_menu, 'yellow')
            print_colored('Input your selection:', 'blue')
            selection = input('')

            if not selection.isdigit():
                print_colored('Wrong input, retry by selecting a number.', 'red')
                continue

            if int(selection) == 0:
                run = False
                continue

            elif int(selection) == 1:
                GoogleCalendarManager().main()
                continue

            elif int(selection) == 2 or int(selection) == 3:
                x = self.campus_selection()

                if int(x) == 0:
                    run = False
                    continue

                elif int(x) == 2:
                    check_in()

                elif int(x) == 3:
                    check_out()
                # call check in or check out


bot = UI()
bot.main()
