import requests
import re


class Blog(object):
    def __init__(self, cookie):
        self.header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "cookie": cookie,
            "referer": "https://i.cnblogs.com/posts",
            "content-type": "application/json;charset=UTF-8",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept": "application/json, text/plain, */*"
        }
        self.result_list = []
        self.resp = ""

    def get_url(self, url, params=None):
        ret = requests.get(url, headers=self.header, params=params)
        return ret

    def blog_categories(self):
        url = "https://i.cnblogs.com/categories"
        resp = self.get_url(url)
        return resp.json()

    def get_blog_url_by_category(self, category):
        url = f"https://i.cnblogs.com/posts"
        params = {
            "categoryid": category.get("CategoryId")
        }
        resp = self.get_url(url, params=params).text
        return resp

    def get_all_title_url(self, data, category):
        ret = []
        titles = re.findall(r'<td class="post-title"><a.*?>(.*?)</a>', data)
        urls = re.findall(r'<td class="post-title"><a href="//(.*?)" id=', data)
        status = re.findall(r'<td class="post-title"><a href=.*?<td>(.*?)</td>', data, re.S)
        for title, url, state in zip(titles, urls, status):
            if state == "发布":
                ret.append({
                    "title": title,
                    "url": url,
                    "state": state,
                })
        self.result_list.append({"name": category.get("Title"), "content": ret})
        return ret

    def gen_html_file(self):
        with open("blog_catalog.html", mode="w", encoding="utf8") as f:
            f.write(self.resp)

    def format_html(self):
        for result in self.result_list:
            pattern = f"""
            <h1>{result.get("name")}</h1>
            <ul>
            """
            for data in result.get("content"):
                pattern += f'<li><a href="https://{data.get("url")}" target="_blank">{data.get("title")}</a></li>'
            pattern += '</ul> '
            self.resp += pattern

    def run(self):
        categories = self.blog_categories()
        for category in categories:
            html = self.get_blog_url_by_category(category)
            self.get_all_title_url(html, category)
        self.format_html()
        self.gen_html_file()


if __name__ == '__main__':
    cookie = "_ga=GA1.1913352542.1560830584; UM_distinctid=16b69c3069b282-06e02fa65d93f2-37677e04-13c680-16b69c3069c802; .CNBlogsCookie=65E4A1AB6BC7590CC93EE149CA71C06668CB396A109B0354EA672996FEF2CFCCACFA63D6C93CC64769C0BE315F00E1B21FA92AB496E9D2BB201A8D00290CFFBA20E290C00E9EE952448A87BEB45B4C355015F6F2; .Cnblogs.AspNetCore.Cookies=CfDJ8D8Q4oM3DPZMgpKI1MnYlrnbT5z10vDnUv8xEu0ttPJ7XH58dYymYlqzaeh-ygyqqEqUzqllBnAWvGJb_JJqkH--8m9iRfm9KgnzLTDUP_MrAc2-cNPflIyNS93vl8FZ8uTaCOlxR1NZuJzBDWOiXF7Qcaq7vwP9qSiesgJERstjlHC_gEZtg5wgk13tJc7GxHRDcedQVLC5dt9NHIZZ_uGmLaTptsYf7UojHxmNq-Xo3NWLOL1uBn9NGnvpz5Efn6q6qqlaYMQuH5W6Vr1BKTHqdRKNZlp2jPWA-gGhJD5TwGk4zQ6tpas8WLsfZLOfznUPx5Q3AnZrqBzfUrOujbIGe6HM50iz8t-ig2glAlPyotU5EIbwRsOxZz-nQXtYzc2yTOkjnId2tgcAVnGo15RBM4Zrs7Q-BIdRBul_NrICU0fLEJkvbC4Nn90UJ312FJVrDC4b-H5UZzgtSeUXnFM; _gid=GA1.2.1703130101.1566183021; SERVERID=a15b3bd10716e69d8be538bb89e87a05|1566533184|1566529948"
    obj = Blog(cookie)
    obj.run()
