from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from PIL import Image


class ArticleColumn(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # 统计浏览次数
    total_views = models.IntegerField(default=0)

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    columns = models.ForeignKey(
        to=ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 调用原有的 save() 方法
        article = super(ArticlePost, self).save()
        print(self.avatar)
        # 固定宽度缩放图片大小
        if self.avatar and not update_fields:   # update_fields排除article_detail中的浏览量增加，提升性能
            print('start')
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article


class ArticleTag(models.Model):
    title = models.CharField(max_length=100)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(to=ArticlePost, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
