from django.urls import path, re_path

from bboard.views import index, by_rubric, BbCreateView, about_us,contacts,add_and_save

app_name = 'bboard'

urlpatterns = [
    # re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    # re_path(r'^add/save/$', add_save, name='add_save'),
    # re_path(r'^add/$', bb_create, name='add'),
    re_path(r'^add/$', add_and_save, name='add'),
    re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, name='by_rubric'),
    re_path(r'^$', index, name='index'),
    path('about/', about_us, name='about'),
    path('contacts/', contacts, name='contacts'),
]
