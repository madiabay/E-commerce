import random

import httpx
from django.http import HttpResponse


class FirstMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print('before first middleware')
        request.my_name = 'Madi'
        """
        middleware полезен когда мы сетим(set) какие то данные до вьюшек(views.py). Чтобы не определять данные 
        на каждом вьюшке.Или можем застопить в каком то мидлваер если данные или что то будет не так.
        НАПРИМЕР:
        """
        num = random.choice([1, 2])
        if num == 1:
            return HttpResponse('ЗАСТОПИЛСЯ')
        response = self._get_response(request)
        # request.my_name = 'Madi' # ЕСЛИ ВОТ ТАК ПОСЛЕ НАПИСАТЬ ТО В SecondMiddleware ЧТО НЕТУ ЭТОТ АТРИБУТ
        print('after first middleware')

        return response


class SecondMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print('before second middleware')
        print(f'{request.my_name=}')
        response = self._get_response(request)
        print('after second middleware')

        return response


class HttpxApiMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.api = httpx
        response = self._get_response(request)

        return response
