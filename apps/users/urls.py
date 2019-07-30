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
from .views import *
urlpatterns = [
    url(r'^info/$', UserinfoView.as_view() ,name='user_info'),

    # 用户上传
    url(r'^image/upload/$', UploadImageView.as_view() ,name='user_image'),

    #用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view() ,name='update_pwd'),

    # 发送邮件验证吗
    url(r'^sendemail_code/$', SendEmailCodeView.as_view() ,name='sendemail_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view() ,name='sendemail_code'),


    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view() ,name='mycourse'),
    # 收到收藏-机构
    url(r'^myfav/org/$', MyFavOrgView.as_view() ,name='myfav_org'),
    # 我的收藏-授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view() ,name='myfav_teacher'),

    url(r'^myfav/course/$', MyFavCourseView.as_view() ,name='myfav_course'),

    url(r'^mymessage/$', MyMessageView.as_view() ,name='mymessage'),


]
