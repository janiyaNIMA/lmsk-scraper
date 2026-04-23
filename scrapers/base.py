import requests

class BaseScraper:
    def __init__(self, session=None):
        self.session = session or requests.Session()
