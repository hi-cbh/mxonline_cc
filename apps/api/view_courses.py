from django.http import JsonResponse
from django.core.exceptions  import ValidationError
from django.views.generic.base import View

from django.contrib.auth import  authenticate
from courses.models import Course, CourseResourse, Video
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q
from operation.models import UserFavorite, CourseComments, UserCourse
from users.forms import LoginForm


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

    def post(self, request):
        '''
        课程详情页
        :param request:
        :param course_id:
        :return:
        将用户get接口，改为post接口仅仅用于接口测试
        '''
        try:
            course_id = request.POST.get("course_id","")

            #user = authenticate(username = user_name ,password = pass_word)

            course = Course.objects.get(id=int(course_id))

            course.click_nums +=1
            course.save()

            courses=[]
            courses.append(
                {
                    "org_name" : course.course_org.name,
                    'teacher' : course.teacher.name,
                    'name' : course.name,
                    'desc' : course.desc,
                    'degree' : course.detail,
                    'learn_times' : course.learn_times,
                    'students' : course.students,
                    'fav_nums' : course.fav_nums,
                    'image' : str(course.image),
                    'click_nums' : course.click_nums,
                    'category' : course.category,
                    'is_banner' : course.is_banner,
                    'youneed_know' : course.youneed_know,
                    'teacher_tell' : course.teacher_tell,
                    'tag' : course.tag,
                    'add_time' : course.add_time
                }
            )




            has_fav_org = False
            has_fav_course = False

            # login_form = LoginForm(request.POST)
            # if login_form.is_valid():
            # user_name = request.POST.get("username","")
            # pass_word = request.POST.get("password","")
            #
            # print("user_name = %s, pass_word = %s" %(user_name,pass_word))
            # user = authenticate(username = user_name ,password = pass_word)


            # if user.is_authenticated():
            #     if UserFavorite.objects.filter(user=request.user,
            #                                    fav_id=course.id, fav_type=1):
            #         has_fav_course = True
            #     if UserFavorite.objects.filter(user=request.user,
            #                                    fav_id=course.course_org.id, fav_type=2):
            #         has_fav_org = True
            #

            tag = course.tag
            if tag:
                relate_courses = Course.objects.filter(~Q(id=course.id),tag=tag)[:1]

                relate_course = []
                for c in relate_courses:
                    relate_course.append(
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
                relate_courses = relate_course


            else:
                relate_courses = []

            return JsonResponse(
                {"status":200,
                 'data':
                     {
                         'course':courses,
                         'relate_courses':relate_courses,
                         'has_fav_course':has_fav_course,
                         'has_fav_org':has_fav_org,
                     }
                 }
                , json_dumps_params={'ensure_ascii':False})
        except BaseException as be:
            return JsonResponse(
                {"status":500,
                 'data':
                     {
                         'msg':be,

                     }
                 }
                , json_dumps_params={'ensure_ascii':False})

class CourseInfoAPIView(View):
    '''课程章节信息'''
    def post(self, request):

        course_id = request.POST.get("course_id","")
        course = Course.objects.get(id=int(course_id))

        course.students +=1
        course.save()

        login_form = LoginForm(request.POST)
        user = None
        if login_form.is_valid():

            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            print("user_name = %s, pass_word = %s" %(user_name,pass_word))
            user = authenticate(username = user_name ,password = pass_word)



        # 查询用户是否已经关联了该课程
        user_cs = UserCourse.objects.filter(user=user, course=course)
        print(user_cs)
        if not user_cs:
            user_course = UserCourse(user=user, course=course)
            user_course.save()



        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # user_in在列表里面
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取最近学过该课程的用户的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResourse.objects.filter(course=course)

        return JsonResponse(
                {"status":200,
                 'data':
                     {
                         'course':course,
                         'all_resources':all_resources,
                         'relate_courses':relate_courses,
                     }
                 }
                , json_dumps_params={'ensure_ascii':False})


class CommentAPIView(View):
    '''课程章节信息'''
    def get(self, request):
        course_id = request.POST.get("course_id","")

        course = Course.objects.get(id=int(course_id))

        login_form = LoginForm(request.POST)
        user = None
        if login_form.is_valid():

            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            print("user_name = %s, pass_word = %s" %(user_name,pass_word))
            user = authenticate(username = user_name ,password = pass_word)


        all_comments = CourseComments.objects.filter(user=user,course=course)


        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # user_in在列表里面
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取最近学过该课程的用户的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResourse.objects.filter(course=course)


        return JsonResponse(
                {"status":200,
                 'data':
                     {
                         'course':course,
                         'all_resources':all_resources,
                         'all_comments':all_comments,
                         'relate_courses':relate_courses,
                     }
                 }
                , json_dumps_params={'ensure_ascii':False})




class AddComentsAPIView(View):
    '''用户评论'''
    def post(self, request):

        login_form = LoginForm(request.POST)
        user = None
        if login_form.is_valid():

            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            print("user_name = %s, pass_word = %s" %(user_name,pass_word))
            user = authenticate(username = user_name ,password = pass_word)


        if user.is_authenticated():
            '''判断用户登录状态'''
            return JsonResponse(
                    {"status":200,
                     'data':
                         {
                             "msg":"用户未登录"
                         }
                     }
                    , json_dumps_params={'ensure_ascii':False})


        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')

        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return JsonResponse(
                {"status":200,
                 'data':
                     {
                         "msg":"添加成功"
                     }
                 }, json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse(
                {"status":200,
                 'data':
                     {
                         "msg":"添加失败"
                     }
                 }, json_dumps_params={'ensure_ascii':False})

class VideoPlayAPIView(View):
    '''视频播放页面'''
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lession.course

        login_form = LoginForm(request.POST)
        user = None
        if login_form.is_valid():

            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")

            print("user_name = %s, pass_word = %s" %(user_name,pass_word))
            user = authenticate(username = user_name ,password = pass_word)

        # 查询用户是否已经关联了该课程
        user_cs = UserCourse.objects.filter(user=user, course=course)
        print(user_cs)
        if not user_cs:
            user_course = UserCourse(user=user, course=course)
            user_course.save()



        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # user_in在列表里面
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取最近学过该课程的用户的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResourse.objects.filter(course=course)

        return JsonResponse(
            {"status":200,
             'data':
                 {
                     'course':course,
                     'all_resources':all_resources,
                     'relate_courses':relate_courses,
                     'video':video,
                 }
             }
            , json_dumps_params={'ensure_ascii':False})
