
from django.conf.urls import url
from apps.api.views_demo import *
from apps.api.view_index import *
from apps.api.view_courses import CourseListAPIView,CourseDetailAPIView
from apps.api.views_user import LoginAPIView

urlpatterns = [
    url(r'^test_demo/',test_demo,name='test_demo'),
    url(r'^index/',index_page,name='index'),
    url(r'^course/',LoginAPIView.as_view(),name='login'),
    url(r'^course/',CourseListAPIView.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailAPIView.as_view(),name="course_detail"),
    url(r'^download_2M/', test_download , name="download2"),
    url(r'^download_1M/', test_download_1M, name="download"),
    url(r'^download_100K/', test_download_1M, name="download3"),

    url(r'^$',test_null,name='test_null'),


]



