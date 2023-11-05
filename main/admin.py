from django.contrib import admin

from main.models import Chat, Message, Profile, Relationship

admin.site.register(Profile)
admin.site.register(Relationship)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
