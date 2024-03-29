from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('register/',views.registerPage,name = "register"),

    path('',views.home,name = "home"),# the name given and tagged name is the url name of the path to access the view of the name inside the quotes
    path('room/<str:id>/',views.room,name = "room"),
    path('profile/<str:id>/',views.userProfile,name="user-profile"),

    path('create-room/',views.createRoom,name = "create-room"),
    path('update-room/<str:id>/',views.updateRoom,name = "update-room"),
    path('delete-room/<str:id>/',views.deleteRoom,name = "delete-room"),
    path('delete-message/<str:id>/',views.deleteMessage,name = "delete-message"),
]