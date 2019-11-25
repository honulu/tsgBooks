from requests import *
from bs4 import BeautifulSoup as bs
import re
import time
import sqlite3
import math
import os


# print iterations progress
def ppBar(iteration, total, prefix= '', suffix = '', decimals = 2, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    # print('\r%s %s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    print('\r%s%s%%' % (bar, percent), end = printEnd)
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
        time.sleep(0.5)
        # print("\033[32;m"++".\033[0m\033[32;m" + lc[i][0]+ " \033[0m\033[34;m"+ lc[i][2]+ " \033[0m\033[36;m" +lc[i][3]+ "\033[0m")
        print("\033[32m{0}.\033[0m\033[32m{1} \033[0m\033[34m{2} \033[0m\033[36m{3} \033[0m".format(str(i+1), lc[i][0], lc[i][2], lc[i][3]))
        
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

        # get the number of book
        ## first get the part of book number
        partOfBookCode = re.findall(r'<font color="red">\d+',content)
        ## then search the number
        numberOfBook = re.findall(r'\d+', partOfBookCode[0])[0]
        
        if numberOfBook == "0":
            print("\033[31;1mNow don't have new book!\033[0m")
            return -1
        else:
            print("\033[mGet the\033[0m\033[34;1m {0} \033[0m\033[mbooks from \033[34;1m{1}\033[0m in \033[34;1m{2}\033[0m.\033[0m".format(numberOfBook, self.__type, self.__time))
            if int(numberOfBook) <= 9:
                bookPages = "1"
            else:
                # bookPages = soup.find("font", attrs={"color":"black"}).string
                bookPages = str(math.ceil(int(numberOfBook)/9))


        # initial Bar
        ## get 
        rows, columns = os.popen('stty size','r').read().split()
        ppBar(0, int(bookPages), prefix = 'Progress:', suffix = 'Complete', length = int(columns)-7)

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
                for tempSoupi in i.p.stripped_strings:
                    self.__bPublish = tempSoupi
                # save bookInformation to bookSqlList
                bookSqlList[tempI][0] = str(self.__bName)
                bookSqlList[tempI][1] = str(self.__bHref)
                bookSqlList[tempI][2] = str(self.__bPublish)
                bookSqlList[tempI][3] = str(self.__bNumber)
                tempI +=1

            SaveDate(bookSqlList, "tsg.db", self.__tableName)
            ppBar(j, int(bookPages), prefix = 'Progress:', suffix = 'Complete', length = int(columns)-7)
def main():
    os.system("clear")
    tableName =str(time.strftime("%Y%m%d%H%M%S",time.localtime()))
    print("\033[mNow time is: \033[0m\033[36;1m%s\033[0m" %(tableName))
    Time = str(input("\033[mType your time: \033[0m"))
    Type = str(input("\033[mType you book list: \033[0m"))
    if Time == "":
        Time = "30"
    if Type == "":
        Type = "TP"
    tableName = Type + tableName + Time
    x = qdtsg(tableName, Time, Type)
    x.fnBook()
    ShowData("tsg.db", tableName)


main()


