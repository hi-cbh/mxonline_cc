from django.db.models import Q
from django.shortcuts import render

# Create your views here.



from django.shortcuts import render

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.views.generic import View
from .models import CourseOrg, Course, CourseResourse,Video
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin



class CourseListView(View):
    '''课程列表'''
    def get(self,request):

        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        #课程搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords)|
                                             Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort',"")

        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html',
                      {
                          'all_courses':courses,
                          'sort':sort,
                          'hot_courses':hot_courses,
                      })


class CourseDetailView(View):
    '''
    课程详情
    '''
    def get(self, request, course_id):

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

        return render(request,'course-detail.html',
                      {
                        'course':course,
                        'relate_courses':relate_courses,
                        'has_fav_course':has_fav_course,
                        'has_fav_org':has_fav_org,
                      })

class CourseInfoView(LoginRequiredMixin,View):
    '''课程章节信息'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.students +=1
        course.save()

        # 查询用户是否已经关联了该课程
        user_cs = UserCourse.objects.filter(user=request.user, course=course)
        print(user_cs)
        if not user_cs:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()



        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # user_in在列表里面
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取最近学过该课程的用户的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResourse.objects.filter(course=course)

        return render(request,'course-video.html',
                      {
                          'course':course,
                          'all_resources':all_resources,
                          'relate_courses':relate_courses,
                      })





class CommentView(LoginRequiredMixin,View):
    '''课程章节信息'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        all_resources = CourseResourse.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)


        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # user_in在列表里面
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取最近学过该课程的用户的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResourse.objects.filter(course=course)


        return render(request,'course-comment.html',
                      {
                          'course':course,
                          'all_resources':all_resources,
                          'all_comments':all_comments,
                          'relate_courses':relate_courses,
                      })


class AddComentsView(View):
    '''用户评论'''
    def post(self, request):

        if not request.user.is_authenticated():
            '''判断用户登录状态'''
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')

        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}',content_type='application/json')



class VideoPlayView(View):
    '''视频播放页面'''
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lession.course
        # 查询用户是否已经关联了该课程
        user_cs = UserCourse.objects.filter(user=request.user, course=course)
        print(user_cs)
        if not user_cs:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()



        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # user_in在列表里面
        # 所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取最近学过该课程的用户的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResourse.objects.filter(course=course)

        return render(request,'course-play.html',
                      {
                          'course':course,
                          'all_resources':all_resources,
                          'relate_courses':relate_courses,
                          'video':video,
                      })

