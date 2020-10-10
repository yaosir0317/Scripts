from enum import Enum
import requests


class MusicAPP(Enum):
    qq = "qq"
    wy = "netease"


PRE_URL = "http://www.musictool.top/"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}


def get_music_list(name, app, page=1):
    data = {"input": name, "filter": "name", "type": app, "page": page}
    resp = requests.post(url=PRE_URL, headers=headers, data=data)
    print(resp.text)
    print(resp.json())


if __name__ == '__main__':
    get_music_list("画", MusicAPP.qq)
