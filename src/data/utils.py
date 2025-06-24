import requests

class Checks:
    def __init__(self):
        pass

    def is_connected(self, url='https://www.google.com'):
        try:
            r = requests.get(url, timeout=5)
            print(200)
            return r.status_code == 200
        except Exception:
            return False

CHECKS = Checks()

