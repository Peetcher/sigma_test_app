from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
import json

from django.views.decorators.csrf import csrf_exempt
from sigma_filter.sigma import facade


def index(request):
    return HttpResponse("Тестовая обработка")


# @csrf_exempt
# def sigma_filter(request):
#     if request.method == 'POST':
#         json_data = request.body.decode('utf-8').replace("'", '"')
#         # очистка по 3 sigma rule
#         result = facade(json.loads(json_data))
#         # возвращаем json
#         return JsonResponse(result, safe=False)
#     else:
#         return HttpResponse('запрос не post')


class Sigma_filter(View):

    def post(self, request):
        json_data = request.body.decode('utf-8').replace("'", '"')
        result = facade(json.loads(json_data))
        return JsonResponse(result, safe=False)
