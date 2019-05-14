import requests
import re
from bs4 import BeautifulSoup
import html
def getSour(url):
    r = requests.get(url, 'html.parsers')
    r.encoding = r.apparent_encoding
    r = html.unescape(r.text)
    return r
def saveFile(d):
    r = open("C:\\Users\\honulu\\Desktop\\code\\python\\tsgBooks\\data\\test.html","w",encoding="utf-8")
    r.
    r.write(d)
    r.close()
def analyWeb(soup):
    k = soup.findAll("div", "list_books")
    for i in k:
        # books's name
        print( re.sub(r'\d*\. ',"",i.h3.get_text()))
        # book's website
        print(re.sub(r"\D", "", i.p.span["id"]))
        # book's publisher
        print(re.sub(r"\s", "", i.p.get_text()))
def main():
    url = "http://172.16.47.83/newbook/newbook_cls_book.php?back_days=15&loca_code=ALL&cls=TP&s_doctype=ALL&clsname=自动化技术、计算机技术&page=2"
    k = getSour(url)
    saveFile(k)

main()
