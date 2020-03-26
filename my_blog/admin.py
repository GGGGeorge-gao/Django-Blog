from django.contrib import admin
from .models import ArticlePost, ArticleColumn, ArticleTag

# Register your models here.
admin.site.register(ArticlePost)

admin.site.register(ArticleColumn)

admin.site.register(ArticleTag)