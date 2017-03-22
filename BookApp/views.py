from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
###################################################################################################


@login_required
def index(request):
    context = Topic.objects.all().values('title')
    return render(request, "Book/index.html", {"title_list":context})


###################################################################################################

def search(request):
    if request.method=="POST":
        title = request.POST.get('title')
        return HttpResponseRedirect(reverse('view-page',kwargs={'topic_name': title}))


###################################################################################################

@login_required
def viewPage(request, topic_name):

    topic_list = Topic.objects.values_list('title', flat=True)
    if topic_name in topic_list:
        obj = AccessLevel.objects.get(user = request.user)
        access_level = obj.access_level
        topic= Topic.objects.get(title=topic_name)
        if topic.min_accessing_level <= access_level:
            return render(request,"Book/view-page.html", {"content":topic})
        else:
            return render(request,"Book/access-denied.html")
    else:
        return HttpResponseRedirect(reverse('page-not-found',kwargs={'topic_name': topic_name}))

###################################################################################################

def pageNotFound(request, topic_name):
    return render(request,"Book/pagenotfound.html",{"topic_name":topic_name})


###################################################################################################

def profileView(request):
    user = User.objects.get(username = request.user)
    obj = AccessLevel.objects.get(user=user)
    access_level = obj.access_level
    return render(request, "Book/profile.html", {"user":user,"access_level":access_level})

###################################################################################################


@login_required
def createPage(request):

    if request.method=="GET":
        form = CreateTopic()
        return render(request, "Book/create-page.html", {"form":form})
    else:
        form = CreateTopic(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view-page', kwargs={'topic_name': request.POST.get('title')}))
        else:
            return render(request, "Book/create-page.html", {"form":form})

###################################################################################################

def deletePage(request):
    if request.method == "GET":
        obj = AccessLevel.objects.get(user=request.user)
        access_level = obj.access_level
        if access_level ==5:
            title_list = Topic.objects.all().values('title')
            return render(request, "Book/delete-page.html", {"title_list": title_list})

    if request.method == "POST":
        title_list = request.POST.getlist('title')
    Topic.objects.filter(title__in=title_list).delete()
    return HttpResponseRedirect(reverse('index'))


###################################################################################################




@login_required
def editPage(request, topic_id=0):

    if request.method=="GET":
        data=Topic.objects.get(topic_id=topic_id)
        form = CreateTopic(instance=data)
        return render(request, "Book/edit-page.html",{"form":form,"id":data.topic_id})

    if request.method=="POST":
        topic_id= request.POST.get('id')
        print('id')
        title = request.POST.get('title')
        print(title)
        content = request.POST.get('content')
        access_level =request.POST.get('min_accessing_level')

        obj = Topic.objects.get(topic_id=topic_id)
        obj.title = title
        obj.content=content
        obj.min_accessing_level=access_level
        obj.save()
        return HttpResponseRedirect(reverse('view-page', kwargs={'topic_name': title}))



###################################################################################################



class addNewUser(LoginRequiredMixin, View):

    def get(self, request):
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
def manageUser(request):
    obj = AccessLevel.objects.get(user=request.user)
    access_level = obj.access_level
    if access_level == 5:
        users = User.objects.all()[1:]
        return render(request, "Book/manage-user.html", {"users":users})
    else:
        return render(request, "Book/access-denied.html")


#####################################################################################################


@login_required
def deleteUser(request, username):
    User.objects.get(username=username).delete()
    return HttpResponseRedirect(reverse('manage-user'))


#####################################################################################################


@login_required
def editUserDetails(request, id=0):
    if request.method == "GET":
        user = User.objects.get(pk=id)
        return render(request,"Book/edit-user-details.html", {"user":user})

    if request.method=="POST":
        user = User.objects.get(pk=request.POST.get('pk'))
        user.username = request.POST.get('username')

        user.email = request.POST.get('email')
        user.save()
        obj = AccessLevel.objects.get(user = user)
        obj.access_level = request.POST.get('access_level')
        obj.save()
        return HttpResponseRedirect(reverse('manage-user'))


#####################################################################################################



def changePassword(request, username=""):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_pass = request.POST.get('new_password1')
        pwd_confirm = request.POST.get('new_password2')
        if new_pass == pwd_confirm:
            user=User.objects.get(username=username)
            user.set_password(new_pass)
            update_session_auth_hash(request, user)
            user.save()
            return HttpResponseRedirect(reverse("manage-user"))
        else:
            return render(request,"accounts/change_password.html", {"form":PasswordChangeForm(request.POST),'error':"Both Passwods Must Match.","username":username})
    else:
        form = PasswordChangeForm(username)
        return render(request, 'accounts/change_password.html', {'form': form,"username":username})


    # djangopass = make_password(old_pass)
    # userpass = User.objects.filter(username=username).values('password')[0]['password']
    # print(djangopass)
    # print(userpass)
    # old_pass = request.POST.get('old_password')
#####################################################################################################






