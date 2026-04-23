from bs4 import BeautifulSoup
from config import Config
from .base import BaseScraper

class EventScraper(BaseScraper):
    def extract(self):
        print("Extracting timeline events...")
        response = self.session.get(Config.DASHBOARD_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        events = []
        
        event_items = soup.select('[data-region="event-item"], .event-list-item, .event')
        for item in event_items:
            name_elem = item.select_one('[data-region="event-name"], .event-name, a')
            course_elem = item.select_one('[data-region="course-name"], .course-name, .small')
            date_elem = item.select_one('[data-region="event-date"], .date')
            
            if name_elem:
                events.append({
                    "name": name_elem.get_text(strip=True),
                    "url": name_elem["href"] if name_elem.has_attr("href") else "",
                    "course_name": course_elem.get_text(strip=True) if course_elem else "Unknown",
                    "due_date": date_elem.get_text(strip=True) if date_elem else "Unknown"
                })
        return events
