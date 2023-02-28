from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt
from sigma_filter.sigma import sigma_clean


def index(request):
    return HttpResponse("Тестовая обработка")


@csrf_exempt
def sigma_filter(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8').replace("'", '"')
        # очистка по 3 sigma rule
        result = sigma_clean(json.loads(json_data))
        # возвращаем json
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('запрос не post')
