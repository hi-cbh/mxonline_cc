from django.http import JsonResponse
from django.core.exceptions  import ValidationError

from courses.models import Course
from organization.models import CourseOrg
from users.models import Banner
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def course_list(request):
    '''课程接口'''
    '''
    参数解析：
    
    搜索关键字<keywords>：搜索字段
    排序方式<sort>：   add_time（默认）、students、click_nums
    
    返回：
    
    '''
    if request.method == 'POST':

        try:

            if not request.POST:
                return JsonResponse(
                    {"status": 500,
                     'msg': "参数错误"
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

            return JsonResponse(
                {"status":200,
                 'data':
                     {
                         'all_courses':courses,
                         'hot_courses':hot_courses,
                     }
                 }
                , json_dumps_params={'ensure_ascii':False})

        except BaseException:
            pass

        return JsonResponse(
            {"status": 500,
             'msg': "参数错误"
             }
            , json_dumps_params={'ensure_ascii':False})