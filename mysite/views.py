from django.http import HttpResponse, HttpRequest
from config.settings import CLIENT_ID
from django.shortcuts import render, redirect
import yadisk
import os


def main(request: HttpRequest) -> HttpResponse:
    """
        Функция стартовой страницы, ожидающая ввода публичной
        ссылки и передающая ее на verify()
    """
    # Быстрая авторизация через Яндекс ID по CLIENT_ID для приложения mycego
    redirect(f'oauth.yandex.ru/authorize?response_type=token&client_id={CLIENT_ID}')
    data = {'public_url': os.getenv('public_url')}
    return render(request, 'index.html', context=data)


def verify(request: HttpRequest) -> HttpResponse:
    """
        Функция проверки публичной ссылки и передающая ее на add_files()
        Поскольку add_files() рекурсивная и нуждается в доступе к переменным,
        оформлена в виде внутренней функции
    """
    public_url = request.GET.get('public_url')
    os.environ['public_url'] = public_url
    yd = yadisk.Client(CLIENT_ID)
    data = {'name': []}

    def add_files(path: str):
        for e in yd.public_listdir(public_url, path=path):
            if e['type'] == 'dir':
                data['name'].append((e['path'][1:], '(folder)', e['file']))
                add_files(e['path'])
            else:
                data['name'].append((e['path'][1:], e['size'], e['file']))

    try:
        yd.get_public_download_link(public_url)
    except:
        return HttpResponse('Неверный или пустой url. Вернитесь назад')

    # Если публичная ссылка указывает на один файл, обрабатываем ее здесь
    if yd.is_public_file(public_url):
        e = yd.get_public_meta(public_url)
        data = {'name': [(e['name'], e['size'], e['file'])]}
    else:
        add_files('')

    return render(request, 'list.html', context=data)


git def ya_verify(request: HttpRequest) -> HttpResponse:
    """
        Функция страницы, на которую перенаправляет Яндекс-служба после регистрации
        нового пользователя данного приложения. В данном случае достаточно CLIENT_ID
    """
    return HttpResponse('Получен токен от нового пользователя')
