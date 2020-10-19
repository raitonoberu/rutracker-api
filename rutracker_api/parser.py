from bs4 import BeautifulSoup
from .torrent import Torrent
from .enums import Url, State


class Parser(object):
    @staticmethod
    def parse_search(raw_html):
        page = BeautifulSoup(raw_html, features="lxml")

        count = int(
            page.find("p", attrs={"class": "med bold"}).contents[0].split(": ")[1]
        )

        nav = page.find("div", attrs={"class": "nav"}).find_all("b")
        if len(nav) != 0:
            page_num = int(nav[0].text)
            total_pages = int(nav[1].text)
        elif count != 0:
            page_num = 1
            total_pages = 1
        else:
            page_num = 0
            total_pages = 0

        items = page.find(id="tor-tbl").find("tbody").find_all("tr")

        result = []
        for item in items:
            info = item.find_all("td")[1:]
            if info == []:
                break
            state = info[0]["title"]
            category = info[1].find("a").text
            title = info[2].find("a").text
            topic_id = int(info[2].find("a")["data-topic_id"])
            author = info[3].find("a").text
            size = int(info[4]["data-ts_text"])
            seeds = int(info[5].find("b").text)
            leeches = int(info[6].text)
            downloads = int(info[7].text)
            registered = int(info[8]["data-ts_text"])

            t = Torrent(
                state=state,
                category=category,
                title=title,
                topic_id=topic_id,
                author=author,
                size=size,
                seeds=seeds,
                leeches=leeches,
                downloads=downloads,
                registered=registered,
            )
            result.append(t)

        return {
            "count": count,
            "page": page_num,
            "total_pages": total_pages,
            "result": result,
        }

    @staticmethod
    def parse_topic(response):
        result = []
        for topic_id, data in response.items():
            result.append(
                Torrent(
                    # author=author, # only id
                    # category=category, # only id
                    # downloads=downloads,
                    # leeches=leeches,
                    registered=data["reg_time"],  # is that timestamp?
                    seeds=data["seeders"],
                    size=int(data["size"]),
                    state=State.get(data["tor_status"]).title,
                    title=data["topic_title"],
                    topic_id=topic_id,
                    hash=data["info_hash"],
                    # magnet=magnet,
                )
            )
        return result
