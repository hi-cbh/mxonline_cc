"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url,include
# from django.contrib import admin
import xadmin
from django.views.static import serve

from djangoProject.settings import MEDIA_ROOT
from users.views import LoginView,LogoutView,RegisterView, ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,ApiView
from users.views import  IndexView
from organization.views import OrgView


urlpatterns = [
    url(r'^api/',include('api.urls', namespace='apis')),
    # url(r'^apis/$', ApiView.as_view() ,name='api'),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(),name='index'),
    url(r'^login/$', LoginView.as_view() ,name='login'),
    url(r'^logout/$', LogoutView.as_view() ,name='logout'),
    url(r'^register/$', RegisterView.as_view() ,name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    url(r'^org/',include('organization.urls', namespace="org")),


    # 课程相关
    url(r'^course/',include('courses.urls', namespace="course")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)',serve, {"document_root":MEDIA_ROOT}),

    # 生成环境的图片
    #url(r'^static/(?P<path>.*)',serve, {"document_root":STATIC_ROOT}),


    url(r'^users/',include('users.urls', namespace="users")),

]

#全局404页面
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
