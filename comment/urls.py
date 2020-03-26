from django.urls import path, re_path
from . import views

urlpatterns = [
    path('post_comment/<int:article_id>', views.post_comment, name='post_comment'),
    path('comment_delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('post_comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
]