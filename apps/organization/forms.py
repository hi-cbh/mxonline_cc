from operation.models import  UserAsk
from django import forms

import re
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2,max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=20)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)



# 使用ModelForm 简化设置form 优化代码
class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ["name","mobile",'course_name']

    def clean_mobile(self):
        print("clean_mobile")
        '''验证手机号码是否合法'''
        mobile = self.cleaned_data['mobile']
        # REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        REGEX_MOBILE = "r1\d{10}"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法",code="mobile_invalid")


