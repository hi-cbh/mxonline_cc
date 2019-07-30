
import xadmin
from xadmin import views


from .models import EmailVerifyRecord,Banner, UserProfile


from xadmin.plugins.auth import UserAdmin


class UserProfileAdmin(UserAdmin):
    pass

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title="慕课网后管理系统"
    site_footer = "慕学管理"
    menu_style='accordion'

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields=['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)


# 这里添加基础设置 - 主题选择
xadmin.site.register(views.BaseAdminView,BaseSetting)
# 这里添加全局
xadmin.site.register(views.CommAdminView,GlobalSettings)