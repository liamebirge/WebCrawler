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
        if (numberVisited == 0):
            title = '----------------------------------\n' + 'SEARCH FOR ' + word + "\n"
        else:
            title = ""

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
            with open('urls.txt', 'a', encoding='utf-8') as file:
                file.write(title + str(numberVisited) + '. Successfully Visited: ' + url + " Word: " + word + "\n")
        except:
            print("Fail")
            with open('urls.txt', 'a', encoding='utf-8') as file:
                file.write(title + str(numberVisited) + '. Failed To Visit: ' + url + " Word: " + word + "\n")
    if foundWord:
        print("The word", word, "was found at", url)
        with open('urls.txt', 'a', encoding='utf-8') as file:
            file.write("The word", word, "was found at", url, '\nTotal Sites Visited: ' + str(numberVisited) + '\nURL Containing Search: ' + url + "\nSearch Term: " + word + "\n------------------------\n")
    else:
        print("The word was not found at specified url")
        with open('urls.txt', 'a', encoding='utf-8') as file:
            file.write("The word was not found at specified url", "\nTotal Sites Visited: " + str(numberVisited) + '\nURL Containing Search: ' + url + "\nSearch Term: " + word + "\n------------------------\n")
