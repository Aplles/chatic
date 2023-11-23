import base64
from functools import lru_cache

from django.core.files.base import ContentFile
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.generic.detail import DetailView
from .forms import *
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q

from .models import *

from django.http import HttpResponse

class ChatListView(View):   #список чатов

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            table = Profile.objects.get(user_id=request.user.id)

            qs = Relationship.objects.invatations_received(table)  # Sent invatations
            results = list(map(lambda x: x.sender, qs))
            is_empty_f = False
            if len(results) == 0:
                is_empty_f = True

            friends_list = table.get_friends()

            user1 = request.user
            qs1 = Profile.objects.get_all_profiles(user1)  # All users

            qs2 = Profile.objects.get_all_profiles_to_invite(user1)  # Available to add users

            user = User.objects.get(username__iexact=user1)
            profile = Profile.objects.get(user=user)
            rel_r = Relationship.objects.filter(sender=profile)
            rel_s = Relationship.objects.filter(receiver=profile)
            rel_receiver = []
            rel_sender = []
            for item in rel_r:
                rel_receiver.append(item.receiver.user)
            for item in rel_s:
                rel_receiver.append(item.sender.user)
            is_empty = False
            if len(qs1) == 0:
                is_empty = True

            return render(request, 'main/chats.html', context={
                'chats': Chat.objects.all(),
                'table': table,
                'qs': results,
                'qs1': qs1, 'qs2': qs2,
                'rel_receiver': rel_receiver,
                'rel_sender': rel_sender,
                'is_empty': is_empty,
                'is_empty_f': is_empty_f,
                'friends_list': friends_list


            })
        return redirect('home')






class ChatSearchView(View): #поиск чата

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            table = Profile.objects.get(user_id=request.user.id)

            qs = Relationship.objects.invatations_received(table)  # Sent invatations
            results = list(map(lambda x: x.sender, qs))
            is_empty_f = False
            if len(results) == 0:
                is_empty_f = True

            friends_list = table.get_friends()

            user1 = request.user
            qs1 = Profile.objects.get_all_profiles(user1)  # All users

            qs2 = Profile.objects.get_all_profiles_to_invite(user1)  # Available to add users

            user = User.objects.get(username__iexact=user1)
            profile = Profile.objects.get(user=user)
            rel_r = Relationship.objects.filter(sender=profile)
            rel_s = Relationship.objects.filter(receiver=profile)
            rel_receiver = []
            rel_sender = []
            for item in rel_r:
                rel_receiver.append(item.receiver.user)
            for item in rel_s:
                rel_receiver.append(item.sender.user)
            is_empty = False
            if len(qs1) == 0:
                is_empty = True

        return render(request, 'main/chats.html', context={
            'chats': Chat.objects.filter(title__icontains=request.GET.get('search')),
            'table': table,
            'qs': results,
            'qs1': qs1, 'qs2': qs2,
            'rel_receiver': rel_receiver,
            'rel_sender': rel_sender,
            'is_empty': is_empty,
            'is_empty_f': is_empty_f,
            'friends_list': friends_list
        })

class ChatsUserListView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            table = Profile.objects.get(user_id=request.user.id)

            qs = Relationship.objects.invatations_received(table)  # Sent invatations
            results = list(map(lambda x: x.sender, qs))
            is_empty_f = False
            if len(results) == 0:
                is_empty_f = True

            friends_list = table.get_friends()

            user1 = request.user
            qs1 = Profile.objects.get_all_profiles(user1)  # All users

            qs2 = Profile.objects.get_all_profiles_to_invite(user1)  # Available to add users

            user = User.objects.get(username__iexact=user1)
            profile = Profile.objects.get(user=user)
            rel_r = Relationship.objects.filter(sender=profile)
            rel_s = Relationship.objects.filter(receiver=profile)
            rel_receiver = []
            rel_sender = []
            for item in rel_r:
                rel_receiver.append(item.receiver.user)
            for item in rel_s:
                rel_receiver.append(item.sender.user)
            is_empty = False
            if len(qs1) == 0:
                is_empty = True


            return render(request, 'main/chats.html', context={
                'chats': Chat.objects.filter(
                    messages_chat__user=request.user.id
                ).annotate(num_messages=Count('messages_chat')).filter(num_messages__gt=0),
                'table': table,
                'qs': results,
                'qs1': qs1, 'qs2': qs2,
                'rel_receiver': rel_receiver,
                'rel_sender': rel_sender,
                'is_empty': is_empty,
                'is_empty_f': is_empty_f,
                'friends_list': friends_list
            })
        return redirect('home')


class ChatDetailView(View):   #открытие чата и просмотр сообщений

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            table = Profile.objects.get(user_id=request.user.id)

            qs = Relationship.objects.invatations_received(table)  # Sent invatations
            results = list(map(lambda x: x.sender, qs))
            is_empty_f = False
            if len(results) == 0:
                is_empty_f = True

            friends_list = table.get_friends()

            user1 = request.user
            qs1 = Profile.objects.get_all_profiles(user1)  # All users

            qs2 = Profile.objects.get_all_profiles_to_invite(user1)  # Available to add users

            user = User.objects.get(username__iexact=user1)
            profile = Profile.objects.get(user=user)
            rel_r = Relationship.objects.filter(sender=profile)
            rel_s = Relationship.objects.filter(receiver=profile)
            rel_receiver = []
            rel_sender = []
            for item in rel_r:
                rel_receiver.append(item.receiver.user)
            for item in rel_s:
                rel_receiver.append(item.sender.user)
            is_empty = False
            if len(qs1) == 0:
                is_empty = True

        chat = Chat.objects.get(id=kwargs['id'])

        return render(request, 'main/chat.html', context={
            'chat': chat,
            'messages': chat.messages_chat.all(),
            'user' : request.user,
            'profile' : Profile.objects.get(user=request.user),
            'table': table,
            'qs': results,
            'qs1': qs1, 'qs2': qs2,
            'rel_receiver': rel_receiver,
            'rel_sender': rel_sender,
            'is_empty': is_empty,
            'is_empty_f': is_empty_f,
            'friends_list': friends_list
        })


class MessageCreateView(APIView):  #отправка сообщений

    @property
    @lru_cache
    def _chat(self):
        try:
            return Chat.objects.get(id=self.request.data.get("chat"))
        except Chat.DoesNotExist:
            return None

    @property
    @lru_cache
    def _user(self):
        try:
            return User.objects.get(id=self.request.data.get("user"))
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_file_base64(file, name):
        if file:
            try:
                format, imgstr = file.split(';base64,')
                return ContentFile(base64.b64decode(imgstr), name=name)
            except Exception as e:
                print(f"Ошибка при декодировании файла: {str(e)}")
        return None

    def post(self, request, *args, **kwargs):
        if not self._chat:
            raise NotFound("Чата не найдено")
        if not self._chat:
            raise NotFound("Пользователя не найдено")
        data = dict(
            message=request.data.get("message"),
            chat=self._chat,
            user=self._user,
        )
        if request.data.get("is_image"):
            data['image'] = self.get_file_base64(
                request.data.get("file_content"),
                request.data.get("file_name"),
            )
        elif not request.data.get("is_image"):
            data['document'] = self.get_file_base64(
                request.data.get("file_content"),
                request.data.get("file_name"),
            )
        Message.objects.create(**data)
        return Response({})


class ProfileDetailView(DetailView): #подробный просмотр профиля
    model = Profile
    template_name = 'main/detail.html'



    # def get_object(self, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_receiver.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['table'] = self.get_object()
        context['created'] = profile.get_date()

        return context

def profile(request):
    if request.user.is_authenticated:

        table = Profile.objects.get(user_id = request.user.id)

        qs = Relationship.objects.invatations_received(table)  #Sent invatations
        results = list(map(lambda x: x.sender, qs))
        is_empty_f = False
        if len(results) == 0:
            is_empty_f = True

        friends_list = table.get_friends()

        user1 = request.user
        qs1 = Profile.objects.get_all_profiles(user1)  #All users



        qs2 = Profile.objects.get_all_profiles_to_invite(user1)  # Available to add users



        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Ваш профиль обновлен')
                return redirect(to='home')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)



        user = User.objects.get(username__iexact=user1)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_receiver.append(item.sender.user)
        is_empty = False
        if len(qs1) == 0:
            is_empty = True



        return render(request, 'main/profile.html', {'user_form': user_form, 'profile_form': profile_form,
                                                     'table' : table, 'qs': results, 'qs1' : qs1, 'qs2' : qs2,
                                                     'rel_receiver' : rel_receiver, 'rel_sender' : rel_sender,
                                                     'is_empty' : is_empty, 'is_empty_f' : is_empty_f,
                                                     'friends_list' : friends_list})
    return render(request, 'main/profile.html')




def send_invatation(request):      #отправить приглашение в друзья
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home')

def remove_from_friends(request):    #удалить из друзей
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('home')


@login_required(login_url='login')
def accept_invatation(request):    # принять запрос в друзья
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('home')
@login_required(login_url='login')
def reject_invatation(request):   # отклонить запрос
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('home')

def register(request):    #регистрация пользователя
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})





class UserLoginView(SuccessMessageMixin, LoginView):    #Вход пользователя в аккаунт
    form_class = LoginForm
    template_name = 'registration/login.html'
    next_page = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context

class UserLogoutView(LogoutView):    #выход из аккаунта
    next_page = 'home'


def create_chat(request):

    if request.method == "POST":
        form = CreateChat(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('home')
    else:

        form = CreateChat()

    context = {'form': form}
    return render(request, 'main/create_chat.html', context)




