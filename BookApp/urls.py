from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.index, name="index"),

    url(r'^search/', views.search, name="search"),

    url(r'^view/page/(?P<topic_name>[A-Za-z0-9 -]+)/$',views.viewPage,name="view-page"),

    url(r'^delete/page/', views.deletePage, name="delete-page"),

    url(r'^create/page/$', views.createPage, name="create-page"),

    url(r'^edit/page/(?P<topic_id>\d+)/$', views.editPage, name="edit-page"),

    url(r'^register/user/$', views.addNewUser.as_view(), name="add-user"),

    url(r'^del/user/(?P<username>\w+)/$', views.deleteUser, name="delete-user"),

    url(r'^manage/user/$', views.manageUser, name="manage-user"),

    url(r'^edit/user/details/(?P<id>\d+)$', views.editUserDetails, name="edit-user-details"),

    url(r'^password/(?P<username>\w+)/$', views.changePassword, name='change_password'),

]

