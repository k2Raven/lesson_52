from django.contrib import admin
from webapp.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'created_at', 'updated_at')

    search_fields = ('title', 'content')
    fields = ('title', 'content',  'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
