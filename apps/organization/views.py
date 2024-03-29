from django.db.models import Q
from django.shortcuts import render

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.views.generic import View

from operation.models import UserFavorite
from .models import CourseOrg, CityDict, Teacher
from django.http import HttpResponse
from .forms import UserAskForm
from courses.models import Course
class OrgView(View):
    '''

    课程机构列表功能
    '''
    def get(self, request):

        #  所有课程
        all_course = Course.objects.all()

        # 课程机构
        course_orgs = CourseOrg.objects.all()

        # 课程数统计
        for org in course_orgs:
            print("org.course_num: ",org.course_num)
            print("org.get_course_nums(): ",org.get_course_nums())
            org.course_num = org.get_course_nums()
            org.save()

        # 热门
        hot_orgs = course_orgs.order_by("-click_nums")[:3]

        #城市
        all_citys = CityDict.objects.all()


        #全局搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            course_orgs = course_orgs.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords))





        # 取出筛选城市
        city_id = request.GET.get('city',"")
        print("city_id: "+city_id)
        if city_id:
            course_orgs = course_orgs.filter(city_id=int(city_id))

        # 取出筛选类别
        category = request.GET.get('category',"")
        print("category: "+category)
        if category:
            course_orgs = course_orgs.filter(category=category)
            for s in course_orgs:
                print(s)

        sort = request.GET.get('sort',"")

        if sort:
            if sort == "students":
                course_orgs = course_orgs.order_by("-students")
            elif sort == "courses":
                course_orgs = course_orgs.order_by("-course_num")


        org_nums = course_orgs.count()

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_orgs,5, request = request)

        orgs = p.page(page)



        return  render(request,'org-list.html',
                       {"course_orgs":orgs,"all_citys":all_citys,
                        'org_nums':org_nums,'city_id':city_id,
                        'category':category,'hot_orgs':hot_orgs ,
                        'sort':sort,'all_course':all_course})
class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):

        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        course_org.click_nums +=1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        print("all_teachers",all_teachers)
        return render(request, 'org-detail-homepage.html',
                      {
                          'all_course':all_courses,
                          'all_teachers':all_teachers,
                          'course_org':course_org,
                          'current_page':current_page,
                          'has_fav':has_fav,
                      })


class OrgCourseView(View):
    '''
    机构课程列表
    '''
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html',
                          {
                              'all_course':all_courses,
                              'course_org':course_org,
                              'current_page':current_page,
                              'has_fav':has_fav,
                          })


class AddUserAskView(View):
    '''用户添加咨询'''
    def post(self,request):
        userask_form = UserAskForm(request.POST)

        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')


class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        return render(request, 'org-detail-desc.html',
                      {
                          'course_org':course_org,
                          'current_page':current_page,
                          'has_fav':has_fav,
                      })

class OrgTeachersView(View):
    '''
    机构教师页
    '''
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        return render(request, 'org-detail-teachers.html',
                      {
                          'course_org':course_org,
                          'all_teachers':all_teachers,
                          'current_page':current_page,
                          'has_fav':has_fav,
                      })


class AddFavView(View):
    '''
    用户收藏，用户取消收藏
    '''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        print("fav_id",fav_id)
        print("fav_type",fav_type)
        if not request.user.is_authenticated():
            '''判断用户登录状态'''
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id), fav_type=int(fav_type))
        print("exist_records",exist_records)
        if exist_records:
            # 如果记录已经存在，则表示用户用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}',content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()




                return HttpResponse('{"status":"success","msg":"已收藏"}',content_type='application/json')

            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}',content_type='application/json')




class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self,request):

        all_teachers = Teacher.objects.all()

        #全局搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                             Q(work_company__icontains=search_keywords)|
                                            Q(work_positon__icontains=search_keywords) )



        # 课程排序
        sort = request.GET.get('sort',"")

        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:5]
        num_teacher = all_teachers.count()
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teachers':sorted_teachers,
            'sort':sort,
            'num_teacher':num_teacher,
        })

class TeacherDetailView(View):

    def get(self, request,teacher_id):

        teachert = Teacher.objects.get(id=int(teacher_id))

        # 点击加1
        teachert.click_nums +=1
        teachert.save()

        all_courses = Course.objects.filter(teacher=teachert)
        sorte_teachers = Teacher.objects.all().order_by('-click_nums')[:5]

        has_teacher_faved=False
        has_org_faved=False
        if request.user.is_authenticated():
            # 未登录状态
            if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teachert.id):
                has_teacher_faved = True
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teachert.org.id):
                has_org_faved = True

        return render(request, 'teacher-detail.html',{
            'teacher':teachert,
            'all_courses':all_courses,
            'sorte_teachers':sorte_teachers,
            'has_org_faved':has_org_faved,
            'has_teacher_faved':has_teacher_faved,
        })
