from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "recipe", "text", "pub_date"]
    list_display_links = ["id", "text"]
