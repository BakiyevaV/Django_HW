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
    print(context)
    obj = context["context"]
    n = None
    for item in obj:
        if item['id'] == 105:
            n = item

    print("Y",n)
    return render(request,'index.html',context)

def object_passport(request,parameter):
    obj = context["context"]
    object = None
    for item in obj:
        if item[parameter] == 105:
            object = item
    return render(request,'object_passport.html',object)
