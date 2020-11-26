from .parser import Parser
from .page_provider import PageProvider
from .api_provider import ApiProvider
from requests import Session
from typing import Union, Optional
from .enums import Sort, Order
from .torrent import Torrent


class RutrackerApi(object):
    def __init__(self, session: Optional[Session] = None):
        if not session:
            session = Session()
        self.parser = Parser()
        self.page_provider = PageProvider(session)
        self.api = ApiProvider(session)

    def login(self, username: str, password: str) -> None:
        """Login Rutracker.org"""

        self.page_provider.login(username, password)

    def search(
        self,
        query: str,
        sort: Union[Sort, str] = "desc",
        order: Union[Order, str] = "registered",
        page: int = 1,
        get_hash: bool = True,
    ) -> dict:
        """Search for torrents. Returns a dictionary with the keys 'count', 'page', 'total_pages' and 'result'"""

        if isinstance(sort, str):
            sort = Sort[sort.upper()].value
        if isinstance(sort, Sort):
            sort = sort.value
        if isinstance(order, str):
            order = Order[order.upper()].value
        if isinstance(order, Order):
            order = order.value

        html = self.page_provider.search(query, sort, order, page)
        results = self.parser.parse_search(html)
        if not get_hash:
            return results
        # get hashes
        ids = [r.topic_id for r in results["result"]]
        hashes = self.api.get_tor_hash(ids)
        for torrent in results["result"]:
            torrent.hash = hashes[str(torrent.topic_id)]
        return results

    def download(self, topic_id: Union[str, int]) -> bytes:
        """Download a .torrent file. Returns bytes"""

        return self.page_provider.torrent_file(topic_id)

    def topic(self, topic_id: Union[str, int]) -> Torrent:
        """Returns information about the torrent"""

        response = self.api.get_tor_topic_data(topic_id)
        return self.parser.parse_topic(response)
