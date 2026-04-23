from bs4 import BeautifulSoup
from config import Config
from .base import BaseScraper

class NotificationScraper(BaseScraper):
    def extract(self):
        print("Extracting notifications...")
        response = self.session.get(Config.DASHBOARD_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        notifications = []
        
        items = soup.select('.notification-item, [data-region="notification-content"]')
        for item in items:
            subject = item.select_one(".subject, .notification-message, h4")
            time = item.select_one(".time, .timestamp, .small")
            if subject:
                notifications.append({
                    "subject": subject.get_text(strip=True),
                    "time": time.get_text(strip=True) if time else "Unknown",
                    "content": item.get_text(strip=True)
                })
                
        if not notifications:
            response = self.session.get(Config.NOTIFICATIONS_URL)
            soup = BeautifulSoup(response.text, "html.parser")
            for item in soup.select(".notification"):
                subject = item.select_one(".subject")
                if subject:
                    notifications.append({
                        "subject": subject.get_text(strip=True),
                        "time": "Unknown",
                        "content": item.get_text(strip=True)
                    })
                    
        return notifications
