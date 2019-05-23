import requests
import re
from bs4 import BeautifulSoup
import html
import sqlite3


# Requests the URL and return text
def getSour(url):
    r = requests.get(url, 'html.parsers')
    r.encoding = r.apparent_encoding
    r = html.unescape(r.text)
    return r

# Save the file to test.html
def saveFile(d):
    r = open("C:\\Users\\honulu\\Desktop\\code\\python\\tsgBooks\\data\\test.html",
             "w", encoding="utf-8")
    r.write(d)
    r.close()


def analyWeb(r, test):
    soup = BeautifulSoup(r, 'html.parser')
    k = soup.findAll("div", "list_books")
    for i in k:
        # books's name
        bookName = re.sub(r'\d*\. ', "", i.h3.get_text())
        # book's website
        bookWebsite = re.sub(r"\D", "", i.p.span["id"])
        # book's publisher
        bookPublisher = re.sub(r"\s", "", i.p.get_text())
        books = bookName + bookPublisher + bookWebsite
        print(books)
        test += 1
        print("***********", test)
    return test
def SaveToSql():
    conn = sqlite3.connect("tsgBooks.db")
    c = conn.cursor()
    c.executemany('''INSERT INTO stocks
                    (bookName, bookWebsite, bookPublisher)''')
    conn.commit()
    conn.close()
def NewDb():
    conn = sqlite3.connect("tsgBooks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE
                (bookName, bookWebsite, bookPublisher)''')
# Get the pages of books
def fUrls(url):
    orign = url
    r = requests.get(orign)
    soup = BeautifulSoup(r.text,'html.parser')
    k = soup.findAll("option")
    n = 0
    for i in k:
        n += 1
    return n


def main():
    url = "http://172.16.47.83/newbook/newbook_cls_book.php?back_days=15&loca_code=ALL&cls=TP&s_doctype=ALL&clsname=自动化技术、计算机技术"
    n = fUrls(url)
    print("all numbers:", n)
    test = 0
    for i in range(1, n+1):
        urls = url + "&page="+ str(i)
        print("NEXT WE WILL %s", urls)
        r = getSour(urls)
        test = analyWeb(r, test)
    print("all books are", test)


main()