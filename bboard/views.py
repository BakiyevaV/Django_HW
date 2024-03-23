import calendar
import json
import os.path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives, send_mail, send_mass_mail, \
    mail_admins

from django.contrib.auth.decorators import user_passes_test
from django.core.serializers import serialize, deserialize
from django.db import transaction
from django.db.models import Count, Max
from django.forms.formsets import ORDERING_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache, cache_control
from django.views.generic import CreateView, DetailView, ListView, DeleteView, ArchiveIndexView, MonthArchiveView, \
    WeekArchiveView, UpdateView
from django.views.generic.base import TemplateView, RedirectView
from precise_bbcode.bbcode import get_parser

from samplesite.settings import BASE_DIR
from .forms import BbForm, CommentsForm, SearchForm
from .models import Bb, Rubric, Comments
from django.forms import modelformset_factory, inlineformset_factory
from django.core.cache import cache, caches
from django.views.decorators.http import condition
from django.utils import timezone

# class Bbslist(ListView):
#     model = Bb
#     template_name = 'index.html'
#     context_object_name = 'bbs'
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt = 0)
#         return context

# class BbIndexView(ArchiveIndexView):
#     model = Bb
#     template_name = 'index.html'
#     date_field = 'published'
#     date_list_period = 'month'
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # updated_date_list = []
#         # for date in context['date_list']:
#         #     month_name = calendar.month_name[date.month]
#         #     updated_date_list.append({
#         #         'year': date.year,
#         #         'month': month_name,
#         #         'day': date.day
#         #     })
#         if 'counter' in self.request.COOKIES:
#             cnt = int(self.request.COOKIES['counter']) + 1
#         else:
#             cnt = 1
#         # context['rubrics'] = Rubric.objects.all()
#         return context

# @cache_page(60 * 5)
def is_updated(request):
    latest_date = Bb.objects.aggregate(Max('updated'))['updated__max']
    latest_date_local = timezone.localtime(latest_date)
    print(latest_date_local)
    return latest_date_local

@condition(last_modified_func=is_updated)
def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    context = {'rubrics': rubrics, 'bbs': bbs }
    response = render(request, 'index.html', context)
    return response

# def index(request):
#     redis = caches['myredis']
#     rubrics_json = redis.get('rubrics')
#     bbs_json = cache.get('bbs')
#
#     if rubrics_json is None:
#         print('no rubrics')
#         rubrics = Rubric.objects.all()
#         rubrics_json = serialize('json', rubrics)  # Сериализация QuerySet в JSON
#         redis.set('rubrics', rubrics_json, timeout=300)
#     else:
#         rubrics = [obj.object for obj in deserialize('json', rubrics_json)]
#
#     if bbs_json is None:
#         print('no bbs')
#         bbs = Bb.objects.all()
#         bbs_json = serialize('json', bbs)
#         cache.set('bbs', bbs_json, timeout=300)
#     else:
#         bbs = [obj.object for obj in deserialize('json', bbs_json)]
#
#     context = {'rubrics': rubrics, 'bbs': bbs }
#     response = render(request, 'index.html', context)
#     return response


# class BbMonthView(MonthArchiveView):
#     model = Bb
#     template_name = 'index.html'
#     date_field = 'published'
#     date_list_period = 'month'
#     month_format = '%m'
#     context_object_name = 'bbs'
#     allow_empty = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         updated_date_list = []
#         for date in context['date_list']:
#             month_name = calendar.month_name[date.month]
#             updated_date_list.append({
#                 'year': date.year,
#                 'month': month_name,
#                 'day': date.day
#             })
#
#         context['date_list'] = updated_date_list
#         context['rubrics'] = Rubric.objects.all()
#         return context



class BbRedirectView(RedirectView):
    url = '/'

class Categorylist(ListView):
    model = Bb
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'
    ordering = ['-published']
    def get_queryset(self, ):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])


class BbCreateView(CreateView, AccessMixin):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.has_perm('bboard.add_bb'):
                return render(request, self.template_name, {'message': 'Нет доступа на создание объявлений'})
            else:
                return render(request, self.template_name, {'form': self.form_class})
        else:
            return redirect_to_login(reverse('bboard:index'))
        return super().get(request, *args, **kwargs)



class AboutUs(TemplateView):
    template_name = 'footer.html'
    content = ["Некоммерческий проект.",
               "Наша цель-построить среду объединяющую продавца и покупателя для их комфортного и безопасного сотрудничества."]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.content
        return context

class Contacts(TemplateView):
    template_name = 'footer.html'
    content = ["сот: + 7 747 777 77 77","Адрес: г.Алматы, ул.Карасай батыра 189 "]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.content
        return context

class BbDetail(DetailView):
    model = Bb
    template_name = 'bb.html'
    context_object_name = 'bb'
    pk_url_kwarg = 'bb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Bb'] = Bb.objects.filter(pk=self.kwargs['bb_id'])
        context['comments'] = Comments.objects.all().filter(bb=self.kwargs['bb_id'])
        return context

def detail(request, pk):
    parser = get_parser()
    bb = Bb.objects.get(pk=pk)
    parsed_content = parser.render(bb.content)
    pass
class CreateComment(CreateView):
    template_name = 'bb.html'
    form_class = CommentsForm
    context_object_name = 'bb'
    pk_url_kwarg = 'bb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bb'] = get_object_or_404(Bb, pk=self.kwargs['bb_id'])
        context['comments'] = Comments.objects.filter(bb=self.kwargs['bb_id'])
        return context

    def form_valid(self, form):
        bb_id = self.kwargs['bb_id']
        bb = get_object_or_404(Bb, pk=bb_id)
        comment = form.save(commit=False)
        comment.bb = bb
        comment.save()
        cache.set('comment', comment, timeout=60)
        cached_comment = cache.get('comment')

        print(cached_comment)

        return redirect(reverse('bboard:detail', args=[bb_id]))

class DeleteComment(DeleteView):
    model = Comments
    template_name = 'bb.html'
    pk_url_kwarg = 'bb_id'
    def get_success_url(self):
        bb_id = self.kwargs['bb_id']
        return reverse('bboard:get_detail', args=[bb_id])
    def get_object(self, queryset=None):
        print(get_object_or_404(Comments, pk=self.kwargs['comment_id']))
        print("айди", self.kwargs['bb_id'])
        return get_object_or_404(Comments, pk=self.kwargs['comment_id'])


class BbEditView(UpdateView):
    template_name = 'update.html'
    model = Bb
    form_class = BbForm

    def get_success_url(self):
        return reverse_lazy('bboard:update', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        messages.add_message(self.request, messages.SUCCESS, 'Изменено')
        return context

def edit(request, bb_id):
    bb = Bb.objects.get(pk=bb_id)
    print(bb)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
                return HttpResponseRedirect(reverse('bboard:by_rubric'), kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk})
            else:
                return HttpResponseRedirect(reverse('bboard:index'))
        else:
            context = {'form': bbf}
            return render(request, 'update.html', context)
    else:
       if request.user.has_perm('bboard.add_bb'):
            bbf = BbForm(instance=bb)
            print(bbf['title'].value())
            context = {'form': bbf}
            return render(request, 'update.html', context)
       else:
           return render(request, 'update.html', {'message': 'Нет доступа на редактирование'})

def commit_handler():
    print('СOMMITED')
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                         can_order=True,
                                         can_delete=True)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in formset:
                if obj.cleaned_data:

                    sp = transaction.savepoint()
                    try:
                        rubric = obj.save(commit=False)
                        rubric.order = obj.cleaned_data[ORDERING_FIELD_NAME]
                        rubric.save()
                        transaction.savepoint_commit(sp)
                    except:
                        transaction.savepoint_rollback(sp)
                        transaction.commit()

                    transaction.on_commit(commit_handler )


            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('bboard:index')

    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'rubrics.html', context)
@user_passes_test(lambda user: user.is_stuff)
def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.user.is_authenticated:
        print(request.user.username)
        if request.method == 'POST':
            formset = BbsFormSet(request.POST, instance=rubric)
            if formset.is_valid():
                formset.save()
                return redirect('bboard:index')
            else:
                formset = BbsFormSet(instance=rubric)
        else:
            formset = BbsFormSet(instance=rubric)
            context = {'formset': formset, 'current_rubric': rubric, 'user': request.user.username}
        return render(request, 'bbs.html', context)
    else:
        print(None)
        formset = BbsFormSet(instance=rubric)
        context = {'formset': formset, 'current_rubric': rubric, 'user': request.user.username}
        return render(request, 'bbs.html', context)


def Search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            current_rubric = sf.cleaned_data['rubric']
            bbs = Bb.objects.filter(title__iregex=keyword, rubric=rubric_id)
            context = {'bbs':bbs, 'rubric': current_rubric, 'keyword': keyword}
            return render(request, 'search_results.html', context)
    else:
        sf = SearchForm()
        context = {'form': sf}
        return render(request, 'search.html', context)

# def my_login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#     else:
#         pass
#
#
# def my_logout(request):
#     logout(request)
#
# def hide_comment(request):
#     if request.user.has_perm('accounts.hide_comment'):
#         pass
# from django.contrib.auth.models import User
# admin = User.objects.get(name='admin')
# if admin.check_password('password'):
#     # дальнейшие действия при совпадении
#     pass
# else:
#     # дальнейшие действия при несовпадении
#     pass

def test_email(request):
    # em = EmailMessage(subject='Test',
    #                   body='Test',
    #                   attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'])


    # em = EmailMessage(subject='Файл',
    #                   body='Файл',
    #                   to=['user@user.com'])
    # em.attach_file(os.path.join(BASE_DIR, 'tmp', 'file.txt'))

    # context = {'user': 'Автор'}
    # s = render_to_string('email/letter.txt', context)
    # em = EmailMessage(subject='Оповещение', body=s, to=['user@user.com'], headers={'Content-Type': 'text/plain; charset=utf-8'})
    # em.send()

    # con = get_connection()
    # con.open()
    # em1 = EmailMessage(subject='Test1', body='Test1', attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'], connection=con)
    # em1.send()
    #
    # em2 = EmailMessage(subject='Test2', body='Test2', attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'], connection=con)
    # em2.send()
    #
    # em3 = EmailMessage(subject='Test3', body='Test3', attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'], connection=con)
    # em3.send()
    # con.close()

    # con = get_connection()
    # con.open()
    # em1 = EmailMessage(subject='Test1', body='Test1', attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'])
    #
    # em2 = EmailMessage(subject='Test2', body='Test2', attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'])
    #
    # em3 = EmailMessage(subject='Test3', body='Test3', attachments=[('password.txt', '123456789', 'text/plain')],
    #                   to=['user@user.com'])
    # con.send.messages([em1, em2, em3])
    # con.close()

    # em = EmailMultiAlternatives(subject='Test1', body='Test1', to=['kim.v.y@mail.ru'])
    # em.attach_alternative('<h1>Test1</h1>', 'text/html')
    # em.send()

    # send_mail('Test1', 'Test1', 'master@.kz', 'user@user.com', html_message='<h1>Test1</h1>')

    # msg1 = ('Test1', 'Test1', 'master@.kz', 'user@user.com', '<h1>Test1</h1>')
    # msg2 = ('Test2', 'Test2', 'master@.kz', 'user@user.com', '<h1>Test1</h1>')
    # msg3 = ('Test3', 'Test3', 'master@.kz', 'user@user.com', '<h1>Test1</h1>')
    # send_mass_mail((msg1, msg2, msg3))

    # user = User.objects.get(username='admin')
    # user.email_user('Test1', 'Test1', fail_silently=True)

    mail_admins('Test1', 'Test1')

    return redirect('bboard:index')




