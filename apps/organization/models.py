from django.db import models

# Create your models here.

from datetime import datetime

class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")


    class Meta:
        verbose_name="城市"
        verbose_name_plural="城市"

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    tag = models.CharField(max_length=20,verbose_name="机构标签", default="全国知名")
    category = models.CharField(default='pxjg',verbose_name='培训类别',max_length=20,choices=(("pxjg","培训机构"),('gr','个人'),('gx','高校')))
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图片",blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, verbose_name="所在城市")
    students = models.IntegerField(default=0,verbose_name='学习人数')
    course_num = models.IntegerField(default=0,verbose_name='课程数')

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural="课程机构"

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        '''获取课程机构教师数量'''
        return self.teacher_set.all().count()

    def get_course_nums(self):
        '''课程数'''
        return self.course_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50,verbose_name="就职公司")
    work_positon = models.CharField(max_length=50,verbose_name="公司职位")
    age = models.IntegerField(default=20,verbose_name="年龄")
    points = models.CharField(max_length=50,verbose_name="教学特点")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    image = models.ImageField(default='',upload_to="teacher/%Y/%m", verbose_name="头像",blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")


    class Meta:
        verbose_name="教师"
        verbose_name_plural="教师"


    def __str__(self):
        return self.name

    def get_course_nums(self):
        '''课程数'''
        return self.course_set.all().count()


