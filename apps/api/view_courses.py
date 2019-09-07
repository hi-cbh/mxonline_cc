from django.http import JsonResponse
from django.core.exceptions  import ValidationError
from django.views.generic.base import View

from django.contrib.auth import  authenticate
from courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q
from operation.models import UserFavorite, CourseComments, UserCourse



class CourseListAPIView(View):
    '''课程接口'''
    '''
    参数解析：
    
    搜索关键字<keywords>：搜索字段
    排序方式<sort>：   add_time（默认）、students、click_nums
    
    返回：
    
    '''
    def post(self, request):
        try:

            if not request.POST:
                return JsonResponse(
                    {"status": 500,
                     'msg': "not request.POST"
                     }
                    , json_dumps_params={'ensure_ascii':False})

            all_courses = Course.objects.all().order_by('-add_time')
            hot_courses = Course.objects.all().order_by('-click_nums')[:3]

            #课程搜索
            search_keywords = request.POST.get('keywords','')
            if search_keywords:
                all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                                 Q(desc__icontains=search_keywords)|
                                                 Q(detail__icontains=search_keywords))

            # 课程排序
            sort = request.POST.get('sort',"")

            if sort:
                if sort == "students":
                    all_courses = all_courses.order_by("-students")
                elif sort == "hot":
                    all_courses = all_courses.order_by("-click_nums")

            try:
                page = request.POST.get('page',1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_courses, 6, request=request)
            courses = p.page(page)


            #QuerySet 需要转为 字典 + list
            course_list1=[]
            for c in all_courses:
                course_list1.append(
                    {
                        "org_name" : c.course_org.name,
                        'teacher' : c.teacher.name,
                        'name' : c.name,
                        'desc' : c.desc,
                        'degree' : c.detail,
                        'learn_times' : c.learn_times,
                        'students' : c.students,
                        'fav_nums' : c.fav_nums,
                        'image' : str(c.image),
                        'click_nums' : c.click_nums,
                        'category' : c.category,
                        'is_banner' : c.is_banner,
                        'youneed_know' : c.youneed_know,
                        'teacher_tell' : c.teacher_tell,
                        'tag' : c.tag,
                        'add_time' : c.add_time
                    }
                )


            course_list2=[]
            for c in hot_courses:
                course_list2.append(
                    {
                        "org_name" : c.course_org.name,
                        'teacher' : c.teacher.name,
                        'name' : c.name,
                        'desc' : c.desc,
                        'degree' : c.detail,
                        'learn_times' : c.learn_times,
                        'students' : c.students,
                        'fav_nums' : c.fav_nums,
                        'image' : str(c.image),
                        'click_nums' : c.click_nums,
                        'category' : c.category,
                        'is_banner' : c.is_banner,
                        'youneed_know' : c.youneed_know,
                        'teacher_tell' : c.teacher_tell,
                        'tag' : c.tag,
                        'add_time' : c.add_time
                    }
                )

            return JsonResponse(
                {"status":200,
                 'data':
                     {
                         'all_courses':course_list1,
                         'hot_courses':course_list2,
                     }
                 }
                , json_dumps_params={'ensure_ascii':False})

        except BaseException as error:

            return JsonResponse(
                {"status": 500,
                 'msg': "参数错误" + str(error)
                 }
                , json_dumps_params={'ensure_ascii':False})



class CourseDetailAPIView(View):

    def get(self, request,course_id):
        '''
            课程详情页
        :param request:
        :param course_id:
        :return:
        '''


        #user = authenticate(username = user_name ,password = pass_word)

        course = Course.objects.get(id=int(course_id))

        course.click_nums +=1
        course.save()


        has_fav_org = False
        has_fav_course = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(~Q(id=course.id),tag=tag)[:1]

        else:
            relate_courses = []

        return JsonResponse(
            {"status":200,
             'data':
                 {
                     'course':course,
                     'relate_courses':relate_courses,
                     'has_fav_course':has_fav_course,
                     'has_fav_org':has_fav_org,
                 }
             }
            , json_dumps_params={'ensure_ascii':False})