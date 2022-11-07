from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.forms import RoomForm, UserForm, MyUserCreationForm
from .models import Topic, Room, Message, User
from django.db.models import Q

# Create your views here.


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.success(request, 'Email does not exist')
            return redirect('login')
        else:
            user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Email or Password is incorrect')

    if request.user.is_authenticated:
        return redirect('home')

    data = {
        'page': page
    }
    return render(request, 'base/login.html', data)


def logoutUser(request):
    logout(request)
    return redirect('home')


def signupUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.username = user.username.lower()
            login(request, user)
            return redirect('home')
        else:
            messages.success(
                request, 'Please fill the required fields in correct format!!!')
    data = {
        'form': form
    }
    return render(request, 'base/signup.html', data)


def home(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )
    # .order_by('-updated','-created')
    topics = Topic.objects.all()[0:3]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    data = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', data)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    # .order_by('-updated','-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    data = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', data)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    data = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html', data)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # This or-->
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
        # <-- This

        # form = RoomForm(request.POST)
        # if form.is_valid:
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
    data = {
        'form': form,
        'topics': topics,
    }
    return render(request, 'base/room_form.html', data)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    data = {
        'form': form,
        'topics': topics,
        'room': room,
    }
    return render(request, 'base/room_form.html', data)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    data = {
        'room': room,
    }
    return render(request, 'base/delete.html', data)


# @login_required(login_url='login')
# def deleteRoom(request, pk):
#     if Room.objects.get(id=pk).delete():
#         messages.success(request, 'Room Deleted Successfully')
#         redirect_back_url = request.META.get('HTTP_REFERER')
#         return redirect('home')
#     else:
#         return redirect('home')


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if message.delete():
        messages = Message.objects.filter(
            room=message.room.id, user=request.user.id)
        if len(messages) == 0:
            message.room.participants.remove(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('room')


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    data = {
        'form': form
    }
    return render(request, 'base/update_user.html', data)


def topicsPage(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains=q)
    )
    data = {
        'topics': topics
    }
    return render(request, 'base/topics.html', data)


def activityPage(request):
    room_messages = Message.objects.all()
    data = {
        'room_messages': room_messages
    }
    return render(request, 'base/activity.html', data)
