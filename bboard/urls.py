from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path
from django.views.decorators.http import condition
from django.views.generic import ArchiveIndexView

from bboard.models import Bb
from bboard.views import BbCreateView, Categorylist, BbDetail, CreateComment, DeleteComment, AboutUs, Contacts, \
     BbRedirectView, BbEditView, edit, rubrics, bbs, Search, index, test_email, is_updated


app_name = 'bboard'

cache_page: object
urlpatterns = [
    re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    re_path(r'^detail/(?P<bb_id>[0-9]+)/$', BbDetail.as_view(), name='detail'),
    path('rubrics/', rubrics, name='rubrics'),
    re_path(r'^rubric/(?P<rubric_id>[0-9]+)/$', Categorylist.as_view(), name='by_rubric'),
    re_path(r'^$', index, name='index'),
    re_path(r'^a\w{3}t/$', AboutUs.as_view(), name='about'),
    re_path(r'^c\w{6}s/$', Contacts.as_view(), name='contacts'),
    re_path(r'^create/(?P<bb_id>[0-9]+)/$', CreateComment.as_view(), name='c_create'),
    re_path(r'^delete/(?P<comment_id>[0-9]+)/(?P<bb_id>[0-9]+)/$', DeleteComment.as_view(), name='delete_comment'),
    path('update/<int:pk>/', edit, name='update'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),
    path('year/<int:year>/', BbRedirectView.as_view(), name='redirect'),
    # path('<int:year>/<int:month>/', BbMonthView.as_view(), name='month'),
    path('mail/', test_email, name='test_email'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),



    path('search/', Search, name='search')
]
