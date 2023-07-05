import os
import io
import urllib.parse
import time
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import Request

##################################################################
def parseUrl(link: str, db):
    req = Request(link, headers={'User-Agent': 'XYZ/3.0'})
    response = None

    while True:
        try:
            response = urllib.request.urlopen(req)
            break
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print("URLErr_code:", e.code)
            if hasattr(e, 'reason'):
                print("URLErr_reason:", e.reason)
            time.sleep(3.0)
            print("<<<")
        except urllib.error.HTTPError as e:
            if hasattr(e, 'code'):
                print("HTTPErr_code:", e.code)
            if hasattr(e, 'reason'):
                print("HTTPErr_reason:", e.reason)
            time.sleep(3.0)
            print("<< <<")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            time.sleep(5.0)
        print("<<")
    ##############################################
    html = response.read()
    raw = BeautifulSoup(html, features="html.parser")

    h1 = raw.find('h1')
    if h1:
    #
        db.write("<item>\n")

        paper = raw.find('div', attrs={'class' : 'paper-abstract'})
        content = paper.find('div', attrs={'class' : 'col-md-12'})
        
        db.write("<h1>" + h1.text.strip() + "</h1>\n")

        items = content.find("p")
        for item in items:
            db.write("<p>" + item.strip() + "</p>\n")

        # tags
        tags = set()
        tags_section = raw.find('div', attrs={'class' : 'paper-tasks'})
        if tags_section:
        #
            tag_class = tags_section.find('div', attrs={'class' : 'col-md-12'})
            if tag_class:
                spans = tag_class.findAll('span', attrs={'class' : 'badge badge-primary'})
                if spans:
                    for span in spans:
                        tag = span.find('span')
                        tags.add(tag.text)
        #
        if len(tags) > 0:
            db.write("<tags>")
            for i in tags:
                db.write(i+";")
            db.write("</tags>\n")
        #
        db.write("<url>"+link+"</url>\n")
        db.write("</item>\n")
    #
    else:
        print("ERROR")
    db.flush()
    pass

##################################################################
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

##################################################################
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
        #time.sleep(1.0)
    #}
    train_db.close()
    fh.close()

##################################################################
def main():
    if False:
        parse()
    else:
        readLinks("paperswithcode-1188709.csv")

##################################################################
if __name__ == "__main__":
    main()
