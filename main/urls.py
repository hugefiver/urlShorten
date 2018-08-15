from django.urls import path, re_path
from . import views


urlpatterns = [
    path('api/getshorten/', views.get_shorten, name='get_shorten_api'),
    path('<str:srt_code>/', views.service_redirect, name='go_to_where'),
    # re_path('^(?P<srt_code>.+/$)', views.service_redirect, name='go_to_where'),
    path('', views.index, name='index_page')
]

