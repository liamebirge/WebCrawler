from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for(key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]
    def getLinks(self, url):
        with open('urls.txt', 'a', encoding='utf-8') as file:
            file.write(url + "\n")
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type') == 'text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode('utf-8')
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "", []

def start():
    print("Please enter the URL, Search Term, Max Pages(def:200):")
    inUrl = input("URL: ")
    inWord = input("Search Term: ")
    inMaxPages = input("Max Pages: ")
    if(inMaxPages == ""):
        inMaxPages = '200'
    input("Press enter to execute search:")
    spider(inUrl, inWord, int(inMaxPages))
        
def spider(url, word, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting: ", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word)>-1:
                foundWord = True
            pagesToVisit = pagesToVisit + links
            print("Success!")
        except:
            print("Fail")
    if foundWord:
        print("The word", word, "was found at", url)
    else:
        print("The word was not found at specified url")
