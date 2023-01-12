from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm



"""rooms= [
    {'id': 1, 'name': "Let's talk scriptures"},
    {'id': 2, 'name': "What is Prayer"},
    {'id': 3, 'name': "As a Christian"},

]"""

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password') #for getting username and password

        try: # checks if user exists
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
       
        user = authenticate(request, username= username,password = password) # name sure credentials are correct

        if user is not None: # get user object on basis of name and password
            login(request,user) # log user in based on credentials and creates a session
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not Exist')
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # we have created a user object after validating the form and when we say commit is false it is to enle us access the user right away
            user.username = user.username.lower() # for purposes of cleaning data, we ensure that all username are converted to lowercase
            user.save() # after username is converted to lower case it is saved
            login(request,user) # then the user automatically is logged in
            return redirect('home') #send user to home page
        else:
            messages.error(request,'An error occured during registration')

    context ={'form':form}
    return render(request,'base/login_register.html',context)
    

def home(request):
    q = request.GET.get('q') if  request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        
        ) # filters all topics down to

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method=="POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') #this body is from room.html template in the division for creating a message
        )
        room.participants.add(request.user) # it is to add creator,or user to the participants list
        return redirect('room',id=room.id)




    context = {'room': room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method=="POST":
        form = RoomForm(request.POST)#passes the data into the form created
        if form.is_valid():#if the data is correct
            form.save()# save it
            return redirect('home')
        print(request.POST)
    context = {'form': form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method=="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context= {'form': form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method=="POST":
        room.delete()
        return redirect("home")

    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method=="POST":
        message.delete()
        return redirect("home")

    return render(request,'base/delete.html',{'obj':message})

