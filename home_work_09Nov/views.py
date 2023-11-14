from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests

def index(request):
    r = requests.get('https://jsonplaceholder.typicode.com/todos/')
    data = r.json()
    new_data = sorted(data, key=lambda x: x["title"], reverse=False)
    global context
    context = {"context": new_data}
    return render(request,'index.html',context)
def object_passport(request, param):
    r = requests.get('https://jsonplaceholder.typicode.com/todos/')
    data = r.json()
    object = None
    for item in data:
        if item["id"] == param:
            object = item
    return render(request,'object_passport.html', {"object":object})
