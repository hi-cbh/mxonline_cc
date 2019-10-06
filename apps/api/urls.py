
from django.conf.urls import url
from apps.api.views_demo import *
from apps.api.view_index import *
from apps.api.view_courses import *
from apps.api.views_user import LoginAPIView

urlpatterns = [
    url(r'^test_demo/',test_demo,name='test_demo'),
    url(r'^index/',index_page,name='index'),
    url(r'^login/',LoginAPIView.as_view(),name='login'),

    # 课程接口
    url(r'^course/',CourseListAPIView.as_view(),name='course_list'),
    # url(r'^course_detail/(?P<course_id>\d+)/$',CourseDetailAPIView.as_view(),name="course_detail"),
    url(r'^course_detail/',CourseDetailAPIView.as_view(),name="course_detail"),
    url(r'^course_info/',CourseInfoAPIView.as_view(),name="course_info"),
    url(r'^comment/',CommentAPIView.as_view(),name="comment"),
    url(r'^add_coments/',AddComentsAPIView.as_view(),name="add_coments"),
    url(r'^video_play/',VideoPlayAPIView.as_view(),name="video_play"),



    url(r'^download_2M/', test_download , name="download2"),
    url(r'^download_1M/', test_download_1M, name="download"),
    url(r'^download_100K/', test_download_100K, name="download3"),

    url(r'^$',test_null,name='test_null'),


]



