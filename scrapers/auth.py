from bs4 import BeautifulSoup
from config import Config
from .base import BaseScraper

class Authenticator(BaseScraper):
    def login(self, username=Config.LMS_USERNAME, password=Config.LMS_PASSWORD):
        response = self.session.get(Config.LOGIN_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        
        token_input = soup.find("input", {"name": "logintoken"})
        if not token_input:
            print("Could not find login token.")
            return False

        fresh_token = token_input["value"]
        print(f"Fetched fresh token: {fresh_token}")

        login_data = {
            "anchor": "",
            "logintoken": fresh_token,
            "username": username,
            "password": password,
            "rememberusername": "1",
        }

        headers = {
            "User-Agent": Config.USER_AGENT,
            "Origin": Config.BASE_URL,
            "Referer": Config.LOGIN_URL,
        }

        response = self.session.post(Config.LOGIN_URL, data=login_data, headers=headers)
        if "login/index.php" in response.url and "loginerrormessage" in response.text:
            print("Login failed.")
            return False
        
        print("Login successful.")
        return True
