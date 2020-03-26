from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_handler, name='index'),
    path('article_list', views.article_list, name='article_list'),  # 博客列表

    path('article_detail/<int:id>/', views.article_detail, name='article_detail'),  # 查看博客详情

    path('article_create/', views.article_create, name='article_create'),  # 创建博客

    path('article_revise/<int:id>/', views.article_revise, name='article_revise'),  # 修改博客
    # path('article_revise/<int:id>/', views.ArticleRevise.as_view(), name='article_revise'),  # 修改博客

    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),  # 删除博客

    path('column_create/', views.column_create, name='column_create'),   # 新建栏目

    # path('tag_create/<int:user_id>', views)

]

