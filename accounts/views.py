from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Clients
from .forms import UserForm, LoginForm
from django.shortcuts import redirect

class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserForm
    model = Clients
    success_url = reverse_lazy('index')
def login_view(request):

    a = Clients.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = None
            users = Clients.objects.all()
            for u in users:
                if u.login == username and u.password == password:
                    user = u
            if user is not None:
                return redirect('index')  # Replace 'main_page' with the actual URL name for your main page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



