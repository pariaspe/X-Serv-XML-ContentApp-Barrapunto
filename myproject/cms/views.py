from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages

# Create your views here.
def barra(request):
    pages = Pages.objects.all()
    lista = '<ul>'
    for page in pages:
        lista += '<li>' + page.name + '</li>'
    lista += '</ul>'
    return HttpResponse(lista)
