from django.db import models
from django.contrib.auth.models import User
from my_blog.models import ArticlePost
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Comment(MPTTModel):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
    )

    reply_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='replyers',
        null=True,
        blank=True,
    )

    class MPTTMeta:
        order_insertion_by = ['created']

