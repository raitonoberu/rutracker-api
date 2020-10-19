# rutracker-api
(Work In Progress)  An easy-to-use package for finding torrents on Rutracker.org

## Installation
```bash
git clone https://github.com/raitonoberu/rutracker-api
cd rutracker-api
pip install -r requirements.txt
cp -r rutracker_api *your project folder*
```

## Usage
```python
>>> from rutracker_api import RutrackerApi
>>> api = RutrackerApi()
>>> api.login("username", "password")
>>> search = api.search("ubuntu mate")
>>> search
{'count': 16, 'page': 1, 'total_pages': 1, 'result': [<Torrent 5956108>, <Torrent 5942849>, <Torrent 5710800>, <Torrent 5560789>, <Torrent 5533679>, <Torrent 5345515>, <Torrent 5336791>, <Torrent 5257800>, <Torrent 5099277>, <Torrent 4358219>, <Torrent 4857137>, <Torrent 4791999>, <Torrent 4692014>, <Torrent 4565546>, <Torrent 4348745>, <Torrent 4144976>]}
>>> result = search['result'][0]
>>> result.title
'[amd64] Ubuntu*Pack 20.04 MATE (сентябрь 2020)'
>>> result.get_magnet()
'magnet:?xt=urn%3Abtih%3AB2EDD8F9A0BEB1368A5EDEBBAB4907B53A69DCCA&tr=http%3A%2F%2Fbt2.t-ru.org%2Fann%3Fmagnet&dn=%5Bamd64%5D+Ubuntu%2APack+20.04+MATE+%28%D1%81%D0%B5%D0%BD%D1%82%D1%8F%D0%B1%D1%80%D1%8C+2020%29&as=http%3A%2F%2Frutracker.org%2Fforum%2Fviewtopic.php%3Ft%3D5956108'
```

## Documentation
Coming soon!
