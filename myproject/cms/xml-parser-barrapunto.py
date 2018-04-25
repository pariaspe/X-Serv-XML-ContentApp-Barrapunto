from urllib import request, error
from xml.sax.handler import ContentHandler

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""
        self.inItem = False
        self.titles = []
        self.links = []

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = 1
            elif name == 'link':
                self.inContent = 1

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'item':
            self.inItem = False
            # sobra?
        if self.inItem:
            if name == 'title':
                self.titles.append(self.theContent)
            elif name == 'link':
                self.links.append(self.theContent)
        if self.inContent:
            self.inContent = 0
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
