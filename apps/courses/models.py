from django.db import models

# Create your models here.

from datetime import datetime

from organization.models import CourseOrg, Teacher

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="课程机构",null=True,blank=True)

    name =models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    teacher = models.ForeignKey(Teacher,verbose_name='讲师', null=True,blank=True)
    degree = models.CharField(verbose_name='难度',choices=(('cj','初级'),('zj','中间'),('gj','高级')),max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums=models.IntegerField(default=0,verbose_name="收藏人数")
    image=models.ImageField(upload_to='courses/%Y/%m',verbose_name="封面图片",blank=True)
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    category = models.CharField(default='后端开发',max_length=20, verbose_name='课程列表')
    is_banner = models.BooleanField(default=False, verbose_name='是否为轮播图')
    youneed_know = models.CharField(default='',max_length=300, verbose_name='课程须知')
    teacher_tell = models.CharField(default='',max_length=300, verbose_name='老师告诉你')
    tag = models.CharField(default='',verbose_name='课程标签',max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")



    class Meta:
        verbose_name="课程"
        verbose_name_plural="课程"

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        '''返回章节数'''
        return self.lession_set.all().count()
    get_zj_nums.short_description='章节数'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lession(self):
        '''获取课程章节'''
        return self.lession_set.all()

class BannerCourse(Course):
    '''xadmin区分轮播视频'''
    class Meta:
        verbose_name="轮播课程"
        verbose_name_plural="轮播课程"
        proxy=True # 重点不分别表

class Lession(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=50,verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name="章节"
        verbose_name_plural="章节"

    def __str__(self):
        return self.name

    def get_lession_video(self):
        '''获取章节视频'''
        return self.video_set.all()


class Video(models.Model):
    lession = models.ForeignKey(Lession, verbose_name="章节")
    name = models.CharField(max_length=50,verbose_name="视频名")
    url = models.CharField(default='',max_length=200, verbose_name='访问地址')
    learn_times = models.IntegerField(default=0, verbose_name='时长（分钟数）')
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name="视频"
        verbose_name_plural="视频"

    def __str__(self):
        return self.name

class CourseResourse(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=50,verbose_name="名称")
    download = models.FileField(upload_to='course/resource/%Y/%m')
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name="课程资源"
        verbose_name_plural="课程资源"

    def __str__(self):
        return self.name
