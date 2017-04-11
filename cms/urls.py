from django.conf.urls import url
from cms import views

urlpatterns = [
    # minutes
    url(r'^minutes/$', views.minutes_list, name='minutes_list'),
    url(r'^minutes/add/$', views.minutes_edit, name='minutes_add'),
    url(r'^minutes/mod/(?P<minutes_id>\d+)/$', views.minutes_edit, name='minutes_mod'),
    url(r'^minutes/del/(?P<minutes_id>\d+)/$', views.minutes_del, name='minutes_del'),

]
