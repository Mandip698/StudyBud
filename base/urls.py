from django.urls import path
from base.views import home, room, createRoom, updateRoom, deleteRoom, loginUser, logoutUser, signupUser, deleteMessage, userProfile, updateUser, topicsPage, activityPage

urlpatterns = [
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('signup/', signupUser, name='signup'),

    path('', home, name="home"),
    path('room/<str:pk>/', room, name="room"),
    path('profile/<str:pk>/', userProfile, name='user-profile'),

    path('create-room/', createRoom, name="create-room"),
    path('update-room/<str:pk>/', updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', deleteMessage, name="delete-message"),
    path('update-user/', updateUser, name='update-user'),
    path('topics/', topicsPage, name='topics'),
    path('activity/', activityPage, name='activity'),
]
