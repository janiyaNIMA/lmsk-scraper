import re
from bs4 import BeautifulSoup
from config import Config
from .base import BaseScraper

class CalendarScraper(BaseScraper):
    def download(self, filename=Config.CALENDAR_FILE, save_file=False):
        print("Downloading calendar...")
        response = self.session.get(Config.CALENDAR_EXPORT_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        
        sesskey_input = soup.find("input", {"name": "sesskey"})
        if not sesskey_input:
            print("Could not find sesskey for calendar export.")
            return None
        sesskey = sesskey_input["value"]
        
        export_data = {
            "sesskey": sesskey,
            "_qf__core_calendar_export_form": "1",
            "events[exportevents]": "all",
            "period[timeperiod]": "recentupcoming",
            "generateurl": "Get calendar URL"
        }
        
        response = self.session.post(Config.CALENDAR_EXPORT_URL, data=export_data)
        
        download_url = None
        ics_link = BeautifulSoup(response.text, "html.parser").find("a", href=lambda x: x and "export_execute.php" in x)
        if ics_link:
            download_url = ics_link["href"]
        
        if not download_url:
            match = re.search(r'https?://[^\s"\']+export_execute\.php[^\s"\']+', response.text)
            if match:
                download_url = match.group(0)

        if not download_url:
            print("Could not find calendar download link.")
            return None

        download_url = download_url.replace("&amp;", "&")
        if "<" in download_url: download_url = download_url.split("<")[0]
        if " " in download_url: download_url = download_url.split(" ")[0]

        if not download_url.startswith("http"):
            download_url = Config.BASE_URL + download_url

        print(f"Downloading .ics from: {download_url}")
        try:
            ics_response = self.session.get(download_url)
            if ics_response.status_code == 200 and b"BEGIN:VCALENDAR" in ics_response.content:
                if save_file:
                    import os
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "wb") as f:
                        f.write(ics_response.content)
                    print(f"Calendar saved to {filename}")
                
                return {
                    "url": download_url,
                    "content": ics_response.content
                }
            else:
                print("Failed to download valid .ics file.")
                return None
        except Exception as e:
            print(f"Error downloading calendar: {e}")
            return None
