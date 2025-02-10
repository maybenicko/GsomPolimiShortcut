import time
from utils.colors import print_colored
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from utils.set_time import get_time


def get_cookies_raw(email, psw):
    _ = True
    while _:
        print_colored(f'\n[ {get_time()} ] [ ATTEMPTING LOGIN... ]', 'yellow')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-logging")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get("https://www.gsom.polimi.it")

            wait = WebDriverWait(driver, 10)
            allow_all_button = wait.until(
                ec.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            allow_all_button.click()

            login_button = wait.until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "div.login-box"))
            )
            login_button.click()

            email_input = WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.ID, "signInName"))
            )
            email_input.send_keys(email)

            pass_input = WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.ID, "password"))
            )
            pass_input.send_keys(psw)

            login_button = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.ID, "next"))
            )
            login_button.click()
            print_colored(f'[ {get_time()} ] [ LOGGING IN... ]', 'yellow')

            """wait = WebDriverWait(driver, 10)
            wait.until(ec.url_to_be("https://www.gsom.polimi.it/flow"))"""
            time.sleep(5)

            driver.get('https://www.gsom.polimi.it/flow/myprograms/')

            wait.until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "a.program-item.d-flex.col-12.my-3.not-underlined"))
            )

            r = driver.page_source
            soup = BeautifulSoup(r, 'lxml')
            program_id = soup.find(
                'a', {'class': 'program-item d-flex col-12 my-3 not-underlined'})['href'].split('?id=')[1]
            cookies = driver.get_cookies()
            _ = False
            print_colored(f'[ {get_time()} ] [ LOGGED IN! ]', 'green')
            return cookies, 'abc6fbc8-3198-ee11-be37-0022489cecab'
        except Exception as e:
            driver.quit()
            print_colored(f'[ {get_time()} ] [ RETRYING LOGIN... ] [{e}]', 'red')
        finally:
            driver.quit()


def good_cookies(email, psw):
    data = get_cookies_raw(email, psw)
    x = data[0]
    program_id = data[1]
    cookie_names = [
        'ai_user', '__Host-next-auth.csrf-token', 'pg_landing_location', '_ga',
        'anonymousToken', 'vvcu', 'vvct', 'CookieConsent', '_gcl_au', '_fbp',
        '_hjSession_4993221', '_tt_enable_cookie', '_ttp', '_clck',
        '__Secure-next-auth.callback-url', 'sc_329hH7W7PR4mIioOy593xR', 'sessionidfl',
        '_hjSessionUser_4993221', 'pg_landing_referrer', 'ai_session',
        '_uetsid', '_uetvid', '_ga_3L6NVXLC5V', '__Secure-next-auth.session-token.0',
        '__Secure-next-auth.session-token.1', '__Secure-next-auth.session-token.2', '_clsk'
    ]

    cookie_parts = []
    for cookie_name in cookie_names:
        for i in x:
            if i and i.get('name') == cookie_name and i.get('value'):
                cookie_parts.append(f"{cookie_name}={i['value']}")

    string_cookie = "; ".join(cookie_parts)
    return string_cookie, program_id


# get_cookies_raw()
