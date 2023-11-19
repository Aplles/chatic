from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('', views.profile, name='home'),


    path('register/', views.register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('chat/search/', ChatSearchView.as_view(), name='chats_search'),
    path('chat/search/remove_friend', remove_from_friends, name='remove_friend'),

    path('chat/', ChatListView.as_view(), name='chats'),
    path('chat/<int:id>/', ChatDetailView.as_view(), name='chat'),

    path('chat/remove_friend', remove_from_friends, name='remove_friend'),

    path('users/chat/', ChatsUserListView.as_view(), name='users_chats'),
    path('users/chat/remove_friend', remove_from_friends, name='remove_friend'),
    path('messages/', MessageCreateView.as_view(), name='messages'),

    path('send_invite/', send_invatation, name='send_invite'),
    path('remove_friend', remove_from_friends, name='remove_friend'),
    path('accept/', accept_invatation, name='accept_invite'),
    path('reject/', reject_invatation, name='reject_invite'),



    path('<slug>/', ProfileDetailView.as_view(), name='profile_detail_view'),
]
