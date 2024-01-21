from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.views.generic.base import TemplateView
from .forms import BbForm,CommentsForm
from .models import Bb, Rubric, Comments

class Bbslist(ListView):
    model = Bb
    template_name = 'index.html'
    context_object_name = 'bbs'
    ordering = ['-published']
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt = 0)
        return context

class Categorylist(ListView):
    model = Bb
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'
    ordering = ['-published']
    def get_queryset(self, ):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

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
        return redirect(reverse('bboard:get_detail', args=[bb_id]))

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










