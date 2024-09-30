from django.urls import path, include
from mysite.apps import MysiteConfig
from mysite.views import main, verify, ya_verify

app_name = MysiteConfig.name

urlpatterns = [
    path('', main, name='mysite'),
    path('verify/', verify, name='verify'),
    path('ya_verify/', ya_verify, name='ya_verify'),
]
