from .enums import Url
from .exceptions import ServerException
from typing import Union
from requests import Session

# More about API: http://api.rutracker.org/v1/docs/


class ApiProvider(object):
    """This class provides access to some official methods of the Rutracker API"""

    def __init__(self, session: Session):
        self.session = session

    def _request(self, endpoint: str, params: dict) -> dict:
        response = self.session.get(Url.API.value + endpoint, params=params)
        json = response.json()
        if "error" in json:
            raise ServerException(json["error"]["text"])
        return json

    def get_peer_stats(self, val: Union[list, str], by: str = "topic_id") -> dict:
        """Get peer stats by topic id (topic_id) or torrent hash (hash)"""

        if isinstance(val, list):
            val = ",".join(map(str, val))

        response = self._request("get_peer_stats", {"by": by, "val": val})
        result = {}
        for key, value in response["result"].items():
            result[key] = {
                "seeders": value[0],
                "leechers": value[1],
                "seeder_last_seen": value[2],
            }
        return result

    def get_topic_id(self, val: Union[list, str]) -> dict:
        """Get topic id by torrent hash"""

        if isinstance(val, list):
            val = ",".join(map(str, val))
        response = self._request("get_topic_id", {"by": "hash", "val": val})
        return response["result"]

    def get_tor_hash(self, val: Union[list, str]) -> dict:
        """Get torrent hash by topic id"""

        if isinstance(val, list):
            val = ",".join(map(str, val))
        response = self._request("get_tor_hash", {"by": "topic_id", "val": val})
        return response["result"]

    def get_tor_topic_data(self, val: Union[list, str]) -> dict:
        """Get torrent topic data by topic id"""

        if isinstance(val, list):
            val = ",".join(map(str, val))
        response = self._request("get_tor_topic_data", {"by": "topic_id", "val": val})
        return response["result"]
