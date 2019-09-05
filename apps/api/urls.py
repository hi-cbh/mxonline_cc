
from django.conf.urls import url
from apps.api.views_demo import *
from apps.api.view_index import *
from apps.api.view_courses import *

urlpatterns = [
    url(r'^test_demo/',test_demo,name='test_demo'),
    url(r'^index/',index_page,name='index'),
    url(r'^course/',course_list,name='course_list'),

    url(r'^$',test_null,name='test_null'),


]



