from django.shortcuts import render
from .models import Human, Child

# Create your views here.
def index(request):
    people = Human.objects.all()
    for human in people:
        if human.children != None:
            human.children = human.children.split(",")
            for child in range(len(human.children)):
                human.children[child] = human.children[child].strip()
    context = {'people':people}
    return render(request, 'index.html', context)

def get_child(request, param):
    children = Child.objects.all()
    child = None
    for c in children:
        if c.name == param:
            child = c
    context = {'child':child}
    return render(request, 'child.html', context)

