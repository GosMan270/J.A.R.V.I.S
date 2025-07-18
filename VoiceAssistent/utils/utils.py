"""
Файл доп утилит которые необходимы, но редко используются
"""
import requests


class Checks:
    """
    Проверки и тесты
    """
    def is_connected(self, url='https://www.google.com'):
        """
        Проверка интернет соединения
        """
        try:
            r = requests.get(url, timeout=5)
            print(200)
            return r.status_code == 200
        except Exception:
            return False


CHECKS = Checks()