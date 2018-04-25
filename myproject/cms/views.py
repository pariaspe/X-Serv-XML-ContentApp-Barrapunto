from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .models import Pages

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
# Create your views here.
barrapunto = {}

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

def print_barrapunto():
    content = ""
    for k,v in barrapunto.items():
        content += "<br/><li><a href='" + v + "'>" + k + "</a></li>"
    return content

def update_barrapunto(_):
    BarrapuntoParser = make_parser()
    BarrapuntoHandler = CounterHandler()
    BarrapuntoParser.setContentHandler(BarrapuntoHandler)

    xmlFile = request.urlopen('http://barrapunto.com/index.rss')
    BarrapuntoParser.parse(xmlFile)

    for i in range(len(BarrapuntoHandler.titles)):
        barrapunto[BarrapuntoHandler.titles[i]] = BarrapuntoHandler.links[i]

    return HttpResponse(print_barrapunto())

def barra(request):
    pages = Pages.objects.all()
    lista = '<ul>'
    for page in pages:
        lista += '<li>' + page.name + '</li>'
    lista += '</ul>'
    return HttpResponse(lista + print_barrapunto())

def otro(request, recurso):
    try:
        page = Pages.objects.get(name=recurso)
        return HttpResponse(page.page + print_barrapunto())
    except Pages.DoesNotExist:
        return HttpResponseNotFound('Pagina no guardada')
