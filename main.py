import json
import os
import time
from datetime import datetime
from config import Config
from scrapers import (
    Authenticator,
    CourseScraper,
    EventScraper,
    NotificationScraper,
    CalendarScraper,
)
from utils import ics_to_json


def main():
    # Ensure data directory exists
    os.makedirs(Config.DATA_DIR, exist_ok=True)

    # Initialize scrapers with a shared session
    auth = Authenticator()
    session = auth.session

    if not auth.login():
        return

    # Use specialized scrapers
    courses_scraper = CourseScraper(session)
    events_scraper = EventScraper(session)
    notifications_scraper = NotificationScraper(session)
    calendar_scraper = CalendarScraper(session)

    data = {
        "metadata": {
            "scraped_at": datetime.now().isoformat(),
            "source": Config.BASE_URL,
        },
        "courses": courses_scraper.extract(),
        "events": events_scraper.extract(),
        "notifications": notifications_scraper.extract(),
        "calendar": {
            "file_path": Config.CALENDAR_FILE,
            "download_url": "",
            "events": [],
        },
    }
    # print(data)

    # Download calendar and parse events directly from content
    calendar_result = calendar_scraper.download(save_file=False)
    if calendar_result:
        data["calendar"]["download_url"] = calendar_result["url"]
        # Parse the ICS content directly without saving to file
        data["calendar"]["events"] = ics_to_json(calendar_result["content"])
        print(f"Parsed {len(data['calendar']['events'])} events from calendar.")

    # Save aggregate data to JSON file
    with open(Config.DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(
        f"Data saved to {Config.DATA_FILE}. Found {len(data['courses'])} courses, {len(data['events'])} events, {len(data['notifications'])} notifications."
    )

    # Post to API if enabled
    if Config.API_ENABLED:
        from api_client import APIClient

        api_client = APIClient(Config.API_URL)
        try:
            api_client.post_calendar_data(data)
            api_client.post_metadata(data["metadata"])
            api_client.post_event_data(data["events"])
            api_client.post_course_data(data["courses"])
        except Exception as e:
            print(f"Error posting data: {e}")
    else:
        print(
            "API posting is disabled. Set API_ENABLED=true in your environment to enable."
        )


if __name__ == "__main__":
    HOURS = 3
    INTERVAL = HOURS * 60 * 60

    while True:
        print(
            f"\n--- Starting Scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---"
        )
        try:
            main()
        except Exception as e:
            print(f"Error during execution: {e}")

        print(f"Scrape completed. Waiting {HOURS} hours for next run...")
        time.sleep(INTERVAL)
