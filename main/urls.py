from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('', views.profile, name='home'),

    # path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='profile'),
    path('register/', views.register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),


    path('chat/', ChatListView.as_view(), name='chats'),
    path('chat/search/', ChatSearchView.as_view(), name='chats_search'),
    path('chat/<int:id>/', ChatDetailView.as_view(), name='chat'),

    path('users/chat/', ChatsUserListView.as_view(), name='users_chats'),
    path('messages/', MessageCreateView.as_view(), name='messages'),

    path('send_invite/', send_invatation, name='send_invite'),
    path('remove_friend', remove_from_friends, name='remove_friend'),
    path('accept/', accept_invatation, name='accept_invite'),
    path('reject/', reject_invatation, name='reject_invite'),



    path('<slug>/', ProfileDetailView.as_view(), name='profile_detail_view'),
]
