from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

###################################################################################################


@login_required
def index(request):
    context = Topic.objects.all().values('title')
    return render(request, "Book/index.html", {"title_list":context})


###################################################################################################


@login_required
def topic(request, topic_name):

    topic_list = Topic.objects.values_list('title', flat=True)

    if topic_name in topic_list:
        obj = AccessLevel.objects.get(user = request.user)
        access_level = obj.access_level
        topic= Topic.objects.get(title=topic_name)
        if topic.min_accessing_level <= access_level:
            return render(request,"Book/topicView.html", {"content":topic})
        else:
            return render(request,"Book/accessdenied.html")
    else:
        return HttpResponseRedirect(reverse('createtopic'))


###################################################################################################


@login_required
def create_topic(request):

    if request.method=="GET":
        form = CreateTopic()
        return render(request, "Book/createTopic.html", {"form":form})
    else:
        form = CreateTopic(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('viewtopic', kwargs={'topic_name': request.POST.get('title')}))
        else:
            return render(request, "Book/createTopic.html", {"form":form})


###################################################################################################


@login_required
def edit_topic(request, topic_id=0):

    if request.method=="GET":
        data=Topic.objects.get(topic_id=topic_id)
        form = CreateTopic(instance=data)
        return render(request, "Book/edittopic.html",{"form":form,"id":data.topic_id})

    if request.method=="POST":
        topic_id= request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        access_level =request.POST.get('min_accessing_level')

        obj = Topic.objects.get(topic_id=topic_id)
        obj.title = title
        obj.content=content
        obj.min_accessing_level=access_level
        obj.save()
        return HttpResponseRedirect(reverse('viewtopic', kwargs={'topic_name': title}))


###################################################################################################


class add_new_user(LoginRequiredMixin, View):

    def get(self, request):
        print("Hello")
        return render(request, "registration/registeruser.html")

    def post(self, request):
        print(request.POST)
        print(request.POST.get('access_level'))
        print(request.POST.get("username"))
        new_user = User.objects.create_user(request.POST.get("username"),request.POST.get("email"),request.POST.get("password"),is_staff=True)
        AccessLevel.objects.create(user = new_user,access_level= int(request.POST.get('access_level')))
        return render(request, "registration/registeruser.html")



#####################################################################################################


@login_required
def user_list(request):
    obj = AccessLevel.objects.get(user=request.user)
    access_level = obj.access_level
    if access_level == 5:
        users = User.objects.all()[1:]
        return render(request, "Book/manageuser.html", {"users":users})
    else:
        return render(request, "Book/accessdenied.html")

#####################################################################################################


@login_required
def delete_user(request, username):
    User.objects.get(username=username).delete()
    return HttpResponseRedirect(reverse('manageuser'))


#####################################################################################################

@login_required
def edit_user(request, id=0):
    if request.method == "GET":
        user = User.objects.get(pk=id)
        return render(request,"Book/edituserdetails.html", {"user":user})

    if request.method=="POST":
        user = User.objects.get(pk=request.POST.get('pk'))
        user.username = request.POST.get('username')

        user.email = request.POST.get('email')
        user.save()
        obj = AccessLevel.objects.get(user = user)
        obj.access_level = request.POST.get('access_level')
        obj.save()
        return HttpResponseRedirect(reverse('manageuser'))

#####################################################################################################


def change_password(request, username=""):
    if request.method == 'POST':
        user=User.objects.get(username=request.POST.get('username'))
        user.set_password(request.POST.get('new_password1'))
        update_session_auth_hash(request, user)
        user.save()
        return HttpResponseRedirect(reverse("manageuser"))
    else:
        form = PasswordChangeForm(username)
        return render(request, 'accounts/change_password.html', {'form': form,"username":username})

#####################################################################################################
# @login_required
# def delete_user(request):
#     if request.method=="GET":
#         obj = AccessLevel.objects.get(user=request.user)
#         access_level = obj.access_level
#         if access_level == 5:
#             users = User.objects.all()
#             return render(request,"Book/deluser.html",{"users":users})
#         else:
#             return render(request, "Book/accessdenied.html")
#     if request.method=="POST":
#         username = request.POST.getlist("username")
#         User.objects.filter(username__in=username).delete()
#         return render(request,"Book/deluser.html",{"users":User.objects.all()})