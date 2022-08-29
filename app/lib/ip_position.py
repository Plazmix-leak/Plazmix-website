import requests


class IpPosition:
    def __init__(self, ip):
        self._ip = ip

        self._city = "Unknown"
        self._country = "Unknown"
        self._region = "Unknown"

        self.__load()

    @property
    def get_city(self):
        return self._city

    @property
    def get_country(self):
        return self._country

    @property
    def get_region(self):
        return self._region

    def __load(self):
        url = f"http://ip-api.com/json/{self._ip}?lang=ru"
        try:
            info = requests.get(url=url).json()
        except Exception:
            info = {}

        self._city = info.get("city", "Неизвестно")
        self._country = info.get("country", "Неизвестно")
        self._region = info.get("regionName", "Неизвестно")

    def get_user_format(self):
        return f"{self._city}, {self._region}, {self._country}"
