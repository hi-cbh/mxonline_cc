import json

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from courses.models import Course
from utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord
# Create your views here.
from django.contrib.auth import  authenticate,login, logout

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import  make_password


from utils.email_send import send_register_email
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm
from organization.models import CourseOrg,Teacher
from operation.models import UserCourse, UserFavorite, UserMessage
from .models import  Banner

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user

        except BaseException as err:
            print(err)
            return None


class RegisterView(View):

    def get(self,request):

        register_form = RegisterForm()
        # register_form.is_valid()
        # print("wtf: "+register_form.email)
        return render(request, 'register.html',{"register_form":register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")

            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html',{'msg':"用户已经存在", "register_form":register_form})

            pass_word = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            print("user_profile.password:" + user_profile.password)
            user_profile.save()


            user_message = UserMessage()
            user_message.user=user_profile.id
            user_message.message = "welcome to user web"
            user_message.save()

            send_register_email(user_name,'register')

            return render(request,"login.html")

        else:
            return render(request,'register.html',{"register_form":register_form})

class LoginView(View):
    def get(self,request):
        return render(request, 'login.html',{})

    def post(self, request):

        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            print("user_name = %s, pass_word = %s" %(user_name,pass_word))
            user = authenticate(username = user_name ,password = pass_word)

            if user is not None:
                # 原理是什么 登录成功后，创建一个session id在服务器，
                if user.is_active:
                    login(request,user)
                    print("login not none")
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request,'login.html',{'msg':'用户未激活'})
            else:
                return render(request, 'login.html',{"msg":"用户名或密码错误"})
        else:
            return render(request, 'login.html',{"login_form":login_form})


class LogoutView(View):
    '''用户登出'''
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class ActiveUserView(View):
    def get(self, request, active_code):
        from django.core.urlresolvers import reverse
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return HttpResponseRedirect(reverse('index'))

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()

        return render(request,'forgetpwd.html',{"forget_form":forget_form})


    def post(self, request):

        forget_form = ForgetForm(request.POST)

        if forget_form.is_valid():
            email = request.POST.get('email',"")
            send_register_email(email,'forget')
            return render(request,'send_success.html')


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        print("ResetView: ")
        if all_records:
            for record in all_records:
                email = record.email

                return render(request, 'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))

class ModifyPwdView(View):
    '''
    修改用户密码，
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)

        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            print("email: "+email)

            if pwd1 != pwd2:
                return render(request, 'password_reset.html',{'email':email,'msg':"密码不一致"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            # user.password = pwd1
            user.save()

            return render(request, 'login.html')

        else:
            email = request.POST.get('email','')
            return render(request, 'password_reset.html',{'email':email})





class UserinfoView(LoginRequiredMixin,View):
    '''用户个人信息'''

    def get(self , request):

        current_page = 'info'

        return render(request, 'usercenter-info.html',
                      {
                          'current_page':current_page,
                      })


    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES,instance=request.user)

        if image_form.is_valid():
            image_form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')




class UpdatePwdView(LoginRequiredMixin,View):
    '''
    个人中心修改用户密码
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)

        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')


            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')

            user = request.user
            user.password = make_password(pwd1)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')




class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    发送邮件验证码
    '''
    def get(self, request):

        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''修改个人邮箱'''
    def post(self, request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email' )
        if existed_records:
            user =request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''
    def get(self, request):
        current_page = 'course'

        user_courses= UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html',
                      {
                            "user_courses":user_courses,
                            "current_page":current_page,
                      })

class MyFavOrgView(LoginRequiredMixin,View):
    '''
    我的课程
    '''
    def get(self, request):

        current_page = 'fav'

        org_list = []
        fav_orgs= UserFavorite.objects.filter(user=request.user, fav_type=2)


        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html',
                      {
                          "org_list":org_list,
                          "current_page":current_page,
                      })

class MyFavTeacherView(LoginRequiredMixin,View):
    '''
    我的收藏-讲师
    '''
    def get(self, request):
        current_page = 'fav'
        teacher_list = []
        fav_teachers= UserFavorite.objects.filter(user=request.user, fav_type=3)


        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html',
                      {
                          "teacher_list":teacher_list,
                          "current_page":current_page,
                      })

class MyFavCourseView(LoginRequiredMixin,View):
    '''
    我的收藏-讲师
    '''
    def get(self, request):
        current_page = 'fav'
        course_list = []
        fav_courses= UserFavorite.objects.filter(user=request.user, fav_type=1)


        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html',
                      {
                          "course_list":course_list,
                          "current_page":current_page,
                      })
class MyMessageView(LoginRequiredMixin,View):
    '''
    我的消息
    '''
    def get(self, request):
        current_page = 'message'

        unreads = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for read in unreads:
            read.has_read = True
            read.save()


        all_message = UserMessage.objects.filter(user=request.user.id)



        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 5, request=request)
        messages = p.page(page)



        return render(request, 'usercenter-message.html',
                      {
                          "messages":messages,
                          "current_page":current_page,
                      })

class IndexView(View):

    def get(self,request):
        all_banners = Banner.objects.all()

        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        banner_org = CourseOrg.objects.all()[:15]

        return render(request, 'index.html',{
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "banner_org":banner_org,
        })


def page_not_found(request):
    '''全局404函数'''
    from django.shortcuts import render_to_response

    response = render_to_response('404.html',{})
    response.status_code=404
    return response


def page_error(request):
    '''全局500函数'''
    from django.shortcuts import render_to_response

    response = render_to_response('500.html',{})
    response.status_code=500
    return response
