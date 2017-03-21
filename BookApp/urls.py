from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^$', views.index, name="index"),

    url(r'topic/(?P<topic_name>\w+)$',views.topic,name="viewtopic"),

    url(r'^create/topic/$', views.create_topic, name="createtopic"),

    url(r'^edit/topic/(?P<topic_id>\d+)/$', views.edit_topic, name="edittopic"),

    url(r'^register/user/$', views.add_new_user.as_view(), name="adduser"),

    url(r'^del/user/(?P<username>\w+)/$', views.delete_user, name="deluser"),

    url(r'^manage/user/$', views.user_list, name="manageuser"),

    url(r'^edit/user/details/(?P<id>\d+)$', views.edit_user, name="edituser"),

    url(r'^password/(?P<username>\w+)/$', views.change_password, name='change_password'),

]

