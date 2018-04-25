from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .models import Pages

# Create your views here.
def barra(request):
    pages = Pages.objects.all()
    lista = '<ul>'
    for page in pages:
        lista += '<li>' + page.name + '</li>'
    lista += '</ul>'
    return HttpResponse(lista)

def otro(request, recurso):
    try:
        page = Pages.objects.get(name=recurso)
        return HttpResponse(page.page)
    except Pages.DoesNotExist:
        return HttpResponseNotFound('Pagina no guardada')
