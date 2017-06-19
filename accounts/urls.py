from django.conf.urls import url
from django.contrib import auth
from . import views

urlpatterns = [
    url(r'^user_registration/$', views.user_registration, name='user_registration'),
    url(r'^user_login/$', views.user_login, name='login'),
    # url(r'^login/(?P<next>\w+)/$', views.login, name='login'),
    # url(r'^logout/$', views.logout, name='logout'),
    url(r'^accounts/login/$', auth.views.login, {'template_name': 'registration/login.html'}),
]