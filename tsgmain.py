from requests import *
from bs4 import BeautifulSoup as bs
import re
import time
from html import unescape
import sqlite3


# print iterations progress
def ppBar(iteration, total, prefix= '', suffix = '', decimals = 3, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s %s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# Create a sqlite database
def CreateBook(fileName, tableName):
    conn = sqlite3.connect(fileName)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS {} (bookName, bookHref, bookPublish, bookNumber)'.format(tableName))
    conn.commit()
    conn.close()

# Save tsgBook data
def SaveDate(data, fileName, tableName):
    conn = sqlite3.connect(fileName)
    c = conn.cursor()
    c.executemany("INSERT INTO {} VALUES (?,?,?,?)".format(tableName), data)
    conn.commit()
    conn.close()

#  show tsgBook data
def ShowData(fileName, tableName):
    conn = sqlite3.connect(fileName)
    c = conn.cursor()
    c.execute('SELECT * FROM {}'.format(tableName))
    lc = c.fetchall()
    for i in range(len(lc)):
        time.sleep(0.2)
        print("\033[32;1m" + lc[i][0]+ "\t\033[0m\033[37;1m"+ lc[i][2]+ "\t\033[0m\033[34;1m" +lc[i][3]+ "\033[0m")
        # print(lc[i][0], lc[i][3], lc[i][2])
    # print(type(c.fetchall()))
    conn.close()

class qdtsg:
    def __init__(self, tableName, time="15", typei="TP"):
        self.__url = "http://172.16.47.83/newbook/newbook_cls_book.php?s_doctype=ALL&loca_code=ALL&back_days="
        self.__time = time
        self.__type = typei
        self.__tableName = tableName
        CreateBook("tsg.db", self.__tableName)
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

        # initial Bar
        ppBar(0, int(bookPages), prefix = 'Progress:', suffix = 'Complete', length = 50)

        # get every book's infornation on every page and print it
        for j in range(1, int(bookPages)+1):
            content = get(self.__url+"page="+str(j)).text
            soup = bs(content, 'html.parser')
            bookList = soup.findAll("div", attrs={"class": "list_books"})
            xxx = len(bookList)
            bookSqlList = [[0 for i in range(4)] for i in range(len(bookList))]
            
            # booklist num
            tempI = 0
            for i in bookList:
                self.__bName = i.a.string
                self.__bHref = re.sub(r"\.{2}","http://172.16.47.83",i.a['href'])
                tempText = i.h3.text
                self.__bNumber = tempText.split()[-1]
                temp = str(i.p.encode("ascii"))
                if "(" in temp:
                    self.__bPublish = unescape(re.findall("\(.*;", temp)[0])
                else:
                    self.__bPublish = unescape(re.findall("&#.*;", temp)[0])
                
                # print(self.__bName, self.__bNumber)
                # save bookInformation to bookSqlList
                bookSqlList[tempI][0] = str(self.__bName)
                bookSqlList[tempI][1] = str(self.__bHref)
                bookSqlList[tempI][2] = str(self.__bPublish)
                bookSqlList[tempI][3] = str(self.__bNumber)
                tempI +=1

            SaveDate(bookSqlList, "tsg.db", self.__tableName)
            ppBar(j, int(bookPages), prefix = 'Progress:', suffix = 'Complete', length = 50)
def main():
    tableName =str(time.strftime("%Y%m%d%H%M%S",time.localtime()))
    print("\033[32;1mNow time is: \033[0m", tableName)
    Time = str(input("\033[32;1mType your time: \033[0m"))
    Type = str(input("\033[32;1mType you book list: \033[0m"))
    if Time == "":
        Time = "30"
    if Type == "":
        Type = "TP"
    tableName = Type + tableName + Time
    x = qdtsg(tableName, Time, Type)
    x.fnBook()
    ShowData("tsg.db", tableName)


main()


