from django.contrib.auth.models import User
from django.db import models
import uuid
from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models import Q
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class Chat(models.Model):  # модель с чатами
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chats_owners',
        verbose_name='Владелец'
    )
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')


class Message(models.Model):  # модель с сообщениями
    message = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Сообщение"
    )
    document = models.FileField(
        null=True,
        blank=True,
        upload_to='documents/',
        verbose_name="Документ"
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/',
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_user",
        verbose_name='Автор сообщения'
    )
    chat = models.ForeignKey(
        "Chat",
        on_delete=models.CASCADE,
        related_name="messages_chat",
        verbose_name='Чат'
    )

    def document_name(self):
        return "".join(self.document.name.split('/')[1:])


class ProfileManager(
    models.Manager):  # класс для управления и получения данных из таблицы Profile (было создано для добавления, удаления из друзей и тп)

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])

        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]

        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):  # модель для ползователей с их доп инфой
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    avatar = models.ImageField(default='profile_images/avatar_site.jpg', upload_to='profile_images', blank=True)
    hobbies = models.TextField(blank=True)
    age = models.PositiveIntegerField(default=18, validators=[MinValueValidator(1), MaxValueValidator(120)], blank=True)
    bio = models.TextField(blank=True)
    aim = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=255, blank=True)

    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile_detail_view", kwargs={"slug": self.slug})

    def get_friends(self):
        a = self.friends.all()
        # a = list(map(a, lambda x: Profile.objects.get(User__id=x.id)))
        # a = []
        # for i in self.friends.all():
        #     a.append(f"{i}")
        return a

    def get_friends_no(self):
        return self.friends.all().count()

    def get_date(self):
        return self.created.date()

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.user)
        self.slug = f'{slugify(self.user)}-{uuid4().hex[:8]}'
        super(Profile, self).save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)


class RelationshipManager(
    models.Manager):  # класс для создания связей между пользователями (для добавления в друзья и прочее)
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):  # модель со связями между пользователями
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
