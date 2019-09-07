from django.http import JsonResponse
from django.core.exceptions  import ValidationError


def test_null(request):
    '''空业务'''
    return JsonResponse({'status':200, "message":"nothing doing"})


def test_demo(request):

    return JsonResponse({'status':200, "message":"ok"})


