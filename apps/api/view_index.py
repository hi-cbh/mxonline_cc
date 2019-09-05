from django.http import JsonResponse
from django.core.exceptions  import ValidationError

from courses.models import Course
from organization.models import CourseOrg
from users.models import Banner


def index_page(request):


    try:
        all_banners = Banner.objects.all()

        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        banner_org = CourseOrg.objects.all()[:15]

        banners=[]
        for r in all_banners:
            banner = {}
            banner["title"] = r.title
            banner["image"] = str(r.image)
            banner["url"] = r.url
            banner["index"] = r.index
            banner["add_time"] = r.add_time
            banners.append(banner)

        course2=[]
        for c in courses:
            course={}
            course["org_name"] = c.course_org.name
            course['teacher'] = c.teacher.name
            course['name']= c.name
            course['desc']= c.desc
            course['degree']= c.detail
            course['learn_times']= c.learn_times
            course['students']= c.students
            course['fav_nums']= c.fav_nums
            course['image']= str(c.image)
            course['click_nums']= c.click_nums
            course['category']= c.category
            course['is_banner']= c.is_banner
            course['youneed_know']= c.youneed_know
            course['teacher_tell']= c.teacher_tell
            course['tag']= c.tag
            course['add_time']= c.add_time

            course2.append(course)

        b_courses=[]
        for bc in banner_courses:
            course = {}
            course["org_name"] = bc.course_org.name
            course['teacher'] = bc.teacher.name
            course['name']= bc.name
            course['desc']= bc.desc
            course['degree']= bc.detail
            course['learn_times']= bc.learn_times
            course['students']= bc.students
            course['fav_nums']= bc.fav_nums
            course['image']= str(bc.image)
            course['click_nums']= bc.click_nums
            course['category']= bc.category
            course['is_banner']= bc.is_banner
            course['youneed_know']= bc.youneed_know
            course['teacher_tell']= bc.teacher_tell
            course['tag']= bc.tag
            course['add_time']= bc.add_time
            b_courses.append(course)

        b_orgs=[]
        for bo in banner_org:
            org={}
            org["name"] = bo.name
            org["desc"] = bo.desc
            org["tag"] = bo.tag
            org["category"] = bo.category
            org["click_nums"] = bo.click_nums
            org["fav_nums"] = bo.fav_nums
            org["image"] = bo.image.__str__()
            org["address"] = bo.address
            org["city"] = bo.city.name
            org["students"] = bo.students
            org["course_num"] = bo.course_num
            org["add_time"] = bo.add_time
            b_orgs.append(org)


        return JsonResponse(
            {"status":200,
             'data':
                 {
                "banners":banners,
                "courses":course2,
                "banner_courses":b_courses,
                "banner_org":b_orgs,
                }
             }
            , json_dumps_params={'ensure_ascii':False})

    except BaseException:
        pass

    return JsonResponse(
        {"status": 500,
         'msg': "数据返回异常"
         }
        , json_dumps_params={'ensure_ascii':False})