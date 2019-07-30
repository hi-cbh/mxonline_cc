from django.db import models

# Create your models here.

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


#继承自带的user
class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50, verbose_name="昵称",default="")
    birday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6,choices=(("male","男"),("female","女")), default="female")
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png",max_length=100,blank=True)

    class Meta:
        verbose_name = '用户类型'
        verbose_name_plural = '用户类型'

    def __str__(self):
        return self.username

    def unread_message_num(self):
        # 只能放在这里，放在开头出现循环调用
        from operation.models import UserMessage
        unread = UserMessage.objects.filter(user = self.id, has_read=False).count()
        print("what ------------ unread", unread)
        return unread


class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=60, verbose_name="验证码")
    email=models.CharField(max_length=50, verbose_name="邮箱")
    send_type=models.CharField(verbose_name="验证码类型",max_length= 20,choices=(("register","注册"),("forget","找回密码"),("update_email","修改邮箱")))
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = '邮箱验证码'
        #表达名字
        verbose_name_plural = '邮箱验证码'

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    '''轮播图'''
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name="轮播图",blank=True)
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")


    class Meta:
        verbose_name = '轮播图'
        #表达名字
        verbose_name_plural = '轮播图'


    def __str__(self):
        return self.title