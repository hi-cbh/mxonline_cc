from django.db import models

# Create your models here.


from datetime import datetime

from users.models import UserProfile
from courses.models import Course



class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name="姓名")
    mobile = models.IntegerField(verbose_name="手机")
    course_name = models.CharField(max_length=50,verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")


    class Meta:
        verbose_name="用户咨询"
        verbose_name_plural="用户咨询"

    def __str__(self):
        return self.name



class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    comments = models.CharField(max_length=200,verbose_name="评论")
    add_time= models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name="课程评论"
        verbose_name_plural="课程评论"


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    fav_id = models.IntegerField(default=0,verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1,"课程"),(2,"课程机构"),(3,"讲师")),default=1,max_length=1)
    add_time= models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name="用户收藏"
        verbose_name_plural="用户收藏"


class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False,verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name="用户消息"
        verbose_name_plural="用户消息"


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name="用户课程"
        verbose_name_plural="用户课程"



