from django.contrib import admin
from webapp.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_filter = ['author']
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'author', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
