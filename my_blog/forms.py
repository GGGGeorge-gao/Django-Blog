from django import forms
from .models import ArticlePost, ArticleColumn, ArticleTag
from django.forms import fields


class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body', 'columns', 'avatar',)
        # exclude = ('tags',)


class ColumnPostForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('title',)


class TagPostForm(forms.ModelForm):

    class Meta:
        model = ArticleTag
        fields = ('title', 'article',)

        # exclude = ('column', 'body',)