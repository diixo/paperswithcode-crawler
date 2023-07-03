import os
import io
import urllib.parse
import time

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import Request


def parseUrl(link: str, db):
    req = Request(link, headers={'User-Agent': 'XYZ/3.0'})
    response = urllib.request.urlopen(req)
    html = response.read()
    raw = BeautifulSoup(html, features="html.parser")

    h1 = raw.find('h1')
    if h1:
        #print(h1.text)
        paper = raw.find('div', attrs={'class' : 'paper-abstract'})
        content = paper.find('div', attrs={'class' : 'col-md-12'})
        
        db.write("<h1>" + h1.text.strip() + "</h1>\n")

        items = content.find("p")
        for item in items:
            #print(item)
            db.write("<p>" + item.strip() + "</p>\n")
    else:
        print("ERROR")
    db.flush()
    pass

def parse():
    train_csv = open("paperswithcode.csv", 'w', encoding='utf-8')

    base = "https://paperswithcode.com/sitemap-papers.xml?p="
    xmls = range(1, 1190)

    urls = set()
    
    for i in xmls:
    #
        link = base + str(i)
        req = Request(link, headers={'User-Agent': 'XYZ/3.0'})

        response = urllib.request.urlopen(req)
        html = response.read()
        raw = BeautifulSoup(html, features="html.parser")

        pages = raw.findAll('loc')
        if pages:
        #
            for page in pages:
            #
                url = page.text
                train_csv.write(url + ";\n")
                urls.add(url)
                print(url + " : " + str(i))
            #
        #
        time.sleep(2.0)
    #

    train_csv.close()
    print("<< urls=" + str(len(urls)))
    pass

def readLinks(strPath):
    train_db = open("paperswithcode.utf8", 'w', encoding='utf-8')
    fh = open(strPath, 'r', encoding='utf-8')
    count = 1

    while True:
    #{
        line = fh.readline()
        if not line:
            break
        line = line.strip(";\n")
        parseUrl(line, train_db)
        print(count)
        count += 1
        time.sleep(1.0)
    #}
    train_db.close()
    fh.close()

def main():
    if False:
        parse()
    else:
        readLinks("paperswithcode-1188709.csv")

if __name__ == "__main__":
    main()
