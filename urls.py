from django.conf.urls import patterns, url

from registration_auth import views

urlpatterns = patterns('',
   url(r'^registration/$', views.registration, name='registration'),
   url(r'^login/$', views.login, name="login"),
   url(r'^logout/$', views.logout, name="logout"),
   url(r'^enter/$', views.auth_page, name="auth_page"),
)
