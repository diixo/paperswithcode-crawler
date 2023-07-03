import os
import io
import urllib.parse
import time

from urllib.request import urlopen
from bs4 import BeautifulSoup

from urllib.parse import urlparse
from urllib.request import Request


def parse(link: str, db):
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

def main():
    train_db = open("paperswithcode.utf8", 'w', encoding='utf-8')

    base = "https://paperswithcode.com/sitemap-papers.xml?p="
    xmls = range(1, 1090)

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
            for page in pages:
                url = page.text
                parse(url, train_db)
                urls.update(url)
                print(url + " : " + str(i))

        print("<< " + str(len(pages)))
        time.sleep(1.0)
    #
    train_db.close()
    print("<< urls=" + str(len(urls)))
    pass


if __name__ == "__main__":
    main()
