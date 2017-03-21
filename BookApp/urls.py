from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.index, name="index"),

    url(r'view/page/(?P<topic_name>\w+)$',views.viewPage,name="viewtopic"),

    url(r'^create/page/$', views.createPage, name="createtopic"),

    url(r'^edit/page/(?P<topic_id>\d+)/$', views.editPage, name="edittopic"),

    url(r'^register/user/$', views.addNewUser.as_view(), name="adduser"),

    url(r'^del/user/(?P<username>\w+)/$', views.deleteUser, name="deluser"),

    url(r'^manage/user/$', views.manageUser, name="manageuser"),

    url(r'^edit/user/details/(?P<id>\d+)$', views.editUserDetails, name="edituser"),

    url(r'^password/(?P<username>\w+)/$', views.changePassword, name='change_password'),

]

