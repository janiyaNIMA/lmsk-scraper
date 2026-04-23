import requests


class APIClient:
    def __init__(self, url):
        self.url = url

    def post_calendar_data(self, data):
        print(f"Posting data to API: {self.url}...")
        try:
            # http://127.0.0.1:5000/calendar
            response = requests.post(
                f"{self.url}/lmsk/calender", json=data["calendar"]["events"], timeout=30
            )
            response.raise_for_status()
            print("Successfully posted data to API.")
            return True
        except Exception as e:
            print(f"Error posting data to API: {e}")
            return False

    def post_metadata(self, metadata):
        print(f"Posting metadata to API: {self.url}/lmsk/metadata...")
        try:
            response = requests.post(
                f"{self.url}/lmsk/metadata", json=metadata, timeout=30
            )
            response.raise_for_status()
            print("Successfully posted metadata to API.")
            return True
        except Exception as e:
            print(f"Error posting metadata to API: {e}")
            return False

    def post_event_data(self, events):
        print(f"Posting events to API: {self.url}/lmsk/event...")
        try:
            response = requests.post(
                f"{self.url}/lmsk/event", json=events, timeout=30
            )
            response.raise_for_status()
            print("Successfully posted events to API.")
            return True
        except Exception as e:
            print(f"Error posting events to API: {e}")
            return False


    def post_course_data(self, courses):
        print(f"Posting courses to API: {self.url}/lmsk/course...")
        try:
            response = requests.post(
                f"{self.url}/lmsk/course", json=courses, timeout=30
            )
            response.raise_for_status()
            print("Successfully posted courses to API.")
            return True
        except Exception as e:
            print(f"Error posting courses to API: {e}")
            return False
