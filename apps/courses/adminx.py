
import xadmin

from .models import Course,Lession,Video,CourseResourse,BannerCourse


class LessionInline(object):
    model = Lession
    extra=0

class CourseResourceInline(object):
    module = CourseResourse
    extra = 0




class UserAskAdmin(object):
    list_display =['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','get_zj_nums']
    search_fields=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    ordering=['-click_nums']
    readonly=['fav_nums']
    # inlines=[LessionInline, CourseResourceInline]


# class BannerUserAskAdmin(object):
#     list_display =['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
#     search_fields=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
#     list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
#
#     ordering=['-click_nums']
#     readonly=['fav_nums']
#     inlines=[LessionInline, CourseResourceInline]
#
#     def queryset(self):
#         qs = super(BannerUserAskAdmin,self).queryset()
#         qs.filter(is_banner=True)
#         return qs


class CourseCommentsAdmin(object):
    list_display = ['course','name','add_time']
    search_fields=['course','name']
    list_filter = ['course','name','add_time']





class UserFavoriteAdmin(object):
    list_display = ['lession','name','add_time']
    search_fields=['lession','name']
    list_filter = ['lession','name','add_time']

class UserMessageAdmin(object):
    list_display =['course','name','download','add_time']
    search_fields=['course','name','download']
    list_filter = ['course','name','download','add_time']


xadmin.site.register(Course,UserAskAdmin)
# xadmin.site.register(BannerCourse,BannerUserAskAdmin)
xadmin.site.register(Lession,CourseCommentsAdmin)
xadmin.site.register(Video,UserFavoriteAdmin)
xadmin.site.register(CourseResourse,UserMessageAdmin)
