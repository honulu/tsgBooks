from requests import *
from bs4 import BeautifulSoup as bs
from html.parser import HTMLParser
import re
class qdtsg:
    def __init__(self, time, typei):
        self.__url = "http://172.16.47.83/newbook/newbook_cls_book.php?s_doctype=ALL&loca_code=ALL&back_days="
        self.__time = time
        self.__type = typei

    def fnBook(self):
        # get the page number
        self.__url += (self.__time+"&cls="+self.__type+"&")
        content = get(self.__url).text
        soup = bs(content, 'html.parser')
        try:
            bookPages = soup.find("font", attrs={"color":"black"}).string
        except :
            print("Now dont have new book")
            return -1
        print(bookPages)
        # get every book's infornation on every page and print it
        for i in range(1, int(bookPages)+1):
            content = get(self.__url+"page="+str(i)).text
            soup = bs(content, 'html.parser')
            bookList = soup.findAll("div", attrs={"class": "list_books"})
            parser = HTMLParser()
            for i in bookList:
                self.__bName = i.a.string
                self.__bHref = re.sub(r"\.{2}","http://172.16.47.83",i.a['href'])
                self.__bPublish = parser.unescape(re.findall("&#.*;", str(i.h3.encode("ascii")))[0])
                temp = str(i.p.encode("ascii"))
                if "(" in temp:
                    self.__bNumber = parser.unescape(re.findall("\(.*;", temp)[0])
                else:
                    self.__bNumber = parser.unescape(re.findall("&#.*;", temp)[0])
                
                print("{} {}".format(self.__bName, self.__bNumber))
            print("***********")
def main():
    time = str(input("Type your time: "))
    Type = str(input("Type you book list: "))
    if time == "":
        time = "30"
    if Type == "":
        Type = "TP"
    x = qdtsg(time, Type)
    x.fnBook()
main()


