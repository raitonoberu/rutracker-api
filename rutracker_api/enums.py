from enum import Enum


class Url(Enum):
    # FORUM
    HOST = "http://rutracker.org"
    LOGIN_URL = HOST + "/forum/login.php"
    SEARCH_URL = HOST + "/forum/tracker.php"
    TOPIC_URL = HOST + "/forum/viewtopic.php"
    DOWNLOAD_URL = HOST + "/forum/dl.php"

    # OTHER
    MAGNET_ANN = "http://bt2.t-ru.org/ann?magnet"
    API = "http://api.rutracker.org/v1/"
    # More about API: http://api.rutracker.org/v1/docs/


class State(Enum):
    # from api.rutracker.org/v1/get_tor_status_titles
    NOT_APPROVED = (0, "не проверено")
    CLOSED = (1, "закрыто")
    APPROVED = (2, "проверено")
    NEED_EDIT = (3, "недооформлено")
    NOT_FORMALIZED = (4, "не оформлено")
    REPEAT = (5, "повтор")
    EMPTY = (6, "")
    CONSUMED = (7, "поглощено")
    DUBIOUSLY = (8, "сомнительно")
    CHECKING = (9, "проверяется")
    TEMPORARY = (10, "временная")
    PREMODERATION = (11, "премодерация")

    def __init__(self, state_id, title):
        self.state_id = state_id
        self.title = title

    @classmethod
    def get(cls, id):
        for state in cls:
            if state.state_id == id:
                return state


class Order(Enum):
    REGISTERED = "1"
    TITLE = "2"
    DOWNLOADS = "4"
    SIZE = "7"
    LASTMESSAGE = "8"
    SEEDS = "10"
    LEECHES = "11"


class Sort(Enum):
    ASC = "1"
    DESC = "2"
