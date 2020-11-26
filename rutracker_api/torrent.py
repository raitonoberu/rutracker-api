from .utils import format_size, generate_magnet
from datetime import datetime
from .enums import Url


class Torrent(object):
    """Stores data about the torrent"""

    def __init__(
        self,
        author=None,
        category=None,
        downloads=None,
        host=None,
        leeches=None,
        registered=None,
        seeds=None,
        size=None,
        state=None,
        title=None,
        topic_id=None,
        hash=None,
        magnet=None,
    ):
        self.author = author
        self.category = category
        self.downloads = downloads
        self.leeches = leeches
        self.registered = registered
        self.seeds = seeds
        self.size = size
        self.state = state
        self.title = title
        self.topic_id = topic_id

        self.url = f"{Url.HOST.value}/forum/viewtopic.php?t={topic_id}"
        self.hash = hash
        self.magnet = magnet

    def formatted_size(self) -> str:
        """Returns the size formated as XXX KB/MB/GB/TB"""

        return format_size(self.size)

    def formatted_registered(self) -> str:
        """Returns the date formatted as YYYY-MM-DD"""

        return datetime.utcfromtimestamp(self.registered).strftime("%Y-%m-%d")

    def get_magnet(self, hash: str = None) -> str:
        """Returns the magnet link. Requires hash"""

        if self.magnet:
            return self.magnet
        if hash:
            self.hash = hash
        if not self.hash:
            raise Exception("No hash provided")

        self.magnet = generate_magnet(
            self.hash, Url.MAGNET_ANN.value, self.title, self.url
        )
        return self.magnet

    def __str__(self):
        return f"[{self.topic_id}] {self.title}"

    def __repr__(self):
        return f"<Torrent {self.topic_id}>"

    def as_dict(self) -> dict:
        return {
            "author": self.author,
            "category": self.category,
            "downloads": self.downloads,
            "leeches": self.leeches,
            "registered": self.registered,
            "seeds": self.seeds,
            "size": self.size,
            "state": self.state,
            "title": self.title,
            "topic_id": self.topic_id,
            "url": self.url,
            "hash": self.hash,
            "magnet": self.magnet,
        }

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __iter__(self):
        return iter(self.as_dict().items())
