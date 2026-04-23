import requests


class APIClient:
    def __init__(self, url):
        self.url = url

    def post_data(self, data):
        print(f"Posting data to API: {self.url}...")
        try:
            # http://127.0.0.1:5000/calendar
            response = requests.post(
                f"{self.url}/lmsk/calendar", json=data["calendar"]["events"], timeout=30
            )
            response.raise_for_status()
            print("Successfully posted data to API.")
            return True
        except Exception as e:
            print(f"Error posting data to API: {e}")
            return False
