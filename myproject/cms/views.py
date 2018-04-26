from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .models import Pages
from .models import Barrapunto
from django.db import IntegrityError

from xml.sax import make_parser
from urllib import request, error
from xml.sax.handler import ContentHandler
# Create your views here.

import cms.parser

def print_barrapunto():
    noticias = Barrapunto.objects.all()
    lista = 'Lista de noticias:<ul>'
    for noticia in noticias:
        lista += '<li><a href="' + noticia.link + '">' + noticia.title + '</a></li>'
    lista += '</ul>'
    return lista

def update_barrapunto(_):
    BarrapuntoParser = make_parser()
    BarrapuntoHandler = cms.parser.CounterHandler()
    BarrapuntoParser.setContentHandler(BarrapuntoHandler)

    xmlFile = request.urlopen('http://barrapunto.com/index.rss')
    BarrapuntoParser.parse(xmlFile)

    for i in range(len(BarrapuntoHandler.titles)):
        noticia = Barrapunto(title=BarrapuntoHandler.titles[i], link=BarrapuntoHandler.links[i])
        try:
            noticia.save()
        except IntegrityError:
            Barrapunto.objects.filter(title=BarrapuntoHandler.titles[i]).update(link=BarrapuntoHandler.links[i])

    return HttpResponse(print_barrapunto())

def barra(request):
    answer = '<h1>Sistema de gestión de contenidos</h1>'
    pages = Pages.objects.all()
    lista = 'Lista de paginas:<ul>'
    for page in pages:
        lista += '<li><a href="' + page.name + '">' + page.name + '</a></li>'
    lista += '</ul>'
    return HttpResponse(answer + lista + print_barrapunto())

def otro(request, recurso):
    try:
        answer = '<h1>Pagina: ' + recurso + '</h1>'
        page = Pages.objects.get(name=recurso)
        return HttpResponse(answer + page.page + '<br/><br/>' + print_barrapunto())
    except Pages.DoesNotExist:
        return HttpResponseNotFound('Pagina no guardada')
