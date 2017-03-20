from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'topic/(?P<topic_name>\w+)$',views.topic,name="viewtopic"),
    url(r'^create/topic/$', views.create_topic, name="createtopic"),
    url(r'^edit/topic/(?P<topic_id>\d+)/$', views.edit_topic, name="edittopic"),
    url(r'^register/user/$', views.add_new_user.as_view(), name="adduser"),
    url(r'^del/user/$', views.delete_user, name="deluser"),
]
