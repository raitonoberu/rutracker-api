from .parser import Parser
from .page_provider import PageProvider
from .api_provider import ApiProvider
from requests import Session


class RutrackerApi(object):
    def __init__(self, session=None):
        if not session:
            session = Session()
        self.parser = Parser()
        self.page_provider = PageProvider(session)
        self.api = ApiProvider(session)

    def login(self, username, password):
        self.page_provider.login(username, password)

    def search(self, query, sort="desc", order="registered", page=1, get_hash=True):
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

    def download(self, topic_id):
        return self.page_provider.torrent_file(topic_id)

    def topic(self, topic_id):
        response = self.api.get_tor_topic_data(topic_id)
        return self.parser.parse_topic(response)
