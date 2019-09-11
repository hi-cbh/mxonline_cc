from django.http import JsonResponse, HttpResponse
from django.core.exceptions  import ValidationError


def test_null(request):
    '''空业务'''
    return JsonResponse({'status':200, "message":"nothing doing"})


def test_demo(request):

    return JsonResponse({'status':200, "message":"ok"})




def test_download(request):
    """
        API文档下载
       :param request:
       :return:
       """
    if request.method == "GET":
        try:
            file = open('static/file/2M.zip', 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
            response['Content-Disposition'] = 'attachment;filename="2M.zip"'
            return response
        except BaseException as error:

            return HttpResponse({"message":"file error"+str(error)})


def test_download_1M(request):
    """
        API文档下载
       :param request:
       :return:
       """
    if request.method == "GET":
        try:
            file = open('static/file/1M.zip', 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
            response['Content-Disposition'] = 'attachment;filename="1M.zip"'
            return response
        except BaseException as error:

            return HttpResponse({"message":"file error"+str(error)})