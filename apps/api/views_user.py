from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth import  authenticate
from apps.users.forms import LoginForm

class LoginAPIView(View):
    '''登录返回一个假token'''
    def get(self,request):
        return JsonResponse(
            {
            "codedata": 10000,
            'msg': "null",
            }
            , json_dumps_params={'ensure_ascii':False}
        )

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
                    # login(request,user)
                    print("login not none")
                    return JsonResponse(
                        {"codedata": 200,
                         'msg': "login success",
                         'token': "true"
                         }
                        , json_dumps_params={'ensure_ascii':False})
                else:
                    return JsonResponse({
                        "codedata": 10001,
                        'msg': "用户未激活",
                        }
                    , json_dumps_params={'ensure_ascii':False}
                    )
            else:
                return JsonResponse({
                    "codedata": 10002,
                    'msg': "用户未激活",
                }
                    , json_dumps_params={'ensure_ascii':False}
                )
        else:
            return JsonResponse({
                "codedata": 10003,
                'msg': "参数错误",
            }
                , json_dumps_params={'ensure_ascii':False}
            )
