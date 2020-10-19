from .enums import Url
from .exceptions import ServerException


class ApiProvider(object):
    def __init__(self, session):
        self.session = session

    def request(self, endpoint, params) -> dict:
        response = self.session.get(Url.API.value + endpoint, params=params)
        json = response.json()
        if "error" in json:
            raise ServerException(json["error"]["text"])
        return json

    def get_peer_stats(self, val, by="topic_id") -> dict:
        """Количество пиров по ID или HASH"""
        if isinstance(val, list):
            val = ",".join(map(str, val))

        response = self.request("get_peer_stats", {"by": by, "val": val})
        result = {}
        for key, value in response["result"].items():
            result[key] = {
                "seeders": value[0],
                "leechers": value[1],
                "seeder_last_seen": value[2],
            }
        return result

    def get_topic_id(self, val) -> dict:
        """ID темы по HASH торрента"""
        if isinstance(val, list):
            val = ",".join(map(str, val))
        response = self.request("get_topic_id", {"by": "hash", "val": val})
        return response["result"]

    def get_tor_hash(self, val) -> dict:
        """HASH торрента по ID темы"""
        if isinstance(val, list):
            val = ",".join(map(str, val))
        response = self.request("get_tor_hash", {"by": "topic_id", "val": val})
        return response["result"]

    def get_tor_topic_data(self, val) -> dict:
        """Данные о раздаче по ID темы"""
        if isinstance(val, list):
            val = ",".join(map(str, val))
        response = self.request("get_tor_topic_data", {"by": "topic_id", "val": val})
        return response["result"]
