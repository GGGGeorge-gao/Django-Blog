from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import decorators
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm
import markdown

from .forms import ArticlePostForm, ColumnPostForm
from .models import ArticlePost, ArticleColumn, ArticleTag


# Create your views here.
def index_handler(request):
    return HttpResponse('404 Not Found XD')


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')

    # 用户搜索操作
    if search:
        articles = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search) |
            Q(author__username__icontains=search) |
            Q(columns__title__icontains=search)
        )

    else:
        # 如果用户没有搜索, search=None 传递到模板会被转换成 "None" 字符串
        search = ''
        # 如果有排序进行处理
        articles = ArticlePost.objects.all()

    if column:
        articles = articles.filter(columns=ArticleColumn.objects.get(title=column))

    if order == 'total_views':
        articles = articles.order_by('-total_views')
    else:
        order = ''

    # 传递给Paginator进行分页
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 传递每篇文章的标签
    for art in articles:
        art.tags = ArticleTag.objects.filter(article_id=art.id)

    context = dict(
        articles=articles,
        order=order,
        search=search,
    )
    # render函数：载入模板，并返回context对象
    return render(request, 'my_blog/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    print(article.avatar)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])  # update_fields表名只有total_views发生改变，提升性能

    # Markdown扩展
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',  # 目录扩展
        ])

    # 筛选评论
    comments = Comment.objects.filter(article=id)
    article.body = md.convert(article.body)  # 处理文章正文
    article.tags = ArticleTag.objects.filter(article_id=id)

    comment_form = CommentForm()

    context = dict(
        article=article,
        toc=md.toc,
        comments=comments,
        comment_form=comment_form,
    )

    return render(request, 'article/detail.html', context)


@decorators.login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST, request.FILES)  # 文件包含文章封面图
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = request.user  # 文章作者

            # 处理文章栏目
            if request.POST['column'] != 'none':
                new_article.columns = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()

            # 创建文章标签
            tags_new = request.POST['tags'].split(';')
            for t in tags_new:
                if t:
                    tag = ArticleTag(title=t, article=ArticlePost.objects.get(id=new_article.id))
                    tag.save()

            return redirect('my_blog:article_list')
        return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()  # 获取所有栏目信息，供下拉栏显示
        context = dict(
            type='创建文章',
            title='',
            body='在此输入...',
            article_form=article_post_form,
            article_column='none',
            columns=columns,
            tags='',
        )
        # 返回模板
        return render(request, 'article/create.html', context)


@decorators.login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("my_blog:article_list")
    else:
        return HttpResponse("本次访问仅允许post请求")


@decorators.login_required(login_url='/userprofile/login/')
def article_revise(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            print(article_post_form.cleaned_data)
            article.title = article_post_form.cleaned_data['title']
            article.body = article_post_form.cleaned_data['body']
            # 修改文章封面图
            print(request.FILES)
            if 'avatar' in request.FILES:
                article.avatar = article_post_form.cleaned_data['avatar']
            # 修改文章栏目
            if request.POST['column'] != 'none':
                article.columns = ArticleColumn.objects.get(id=request.POST['column'])
            article.save()

            # 修改标签，剔除旧标签，增加新标签
            tags_old = list(map(lambda a: a.title, list(ArticleTag.objects.filter(article_id=id))))
            tags_new = request.POST['tags'].split(';')

            tags_delete = [t for t in tags_old if t not in tags_new]  # 应删除的标签
            tags_add = [t for t in tags_new if t not in tags_old]  # 应新增加的标签
            for t in tags_delete:
                ArticleTag.objects.get(article_id=id, title=t).delete()
            for t in tags_add:
                if t:
                    tag = ArticleTag(title=t, article=ArticlePost.objects.get(id=id))
                    tag.save()

            return redirect('my_blog:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    else:
        article_revise_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = dict(
            type='修改文章',
            title=article.title,
            body=article.body,
            article_form=article_revise_form,
            article_column=article.columns,
            columns=columns,
            tags=';'.join(list(map(lambda a: a.title, list(ArticleTag.objects.filter(article_id=id))))),  # 所有标签字符串
        )
        return render(request, 'article/create.html', context)


def column_create(request):
    if request.method == 'POST':
        column_form = ColumnPostForm(data=request.POST)
        if column_form.is_valid():
            column_form.save()
            return redirect("my_blog:article_list")
        else:
            return HttpResponse("表单信息填写有误，请重新填写！")
    else:
        column_form = ColumnPostForm()
        context = dict(
            column_form=column_form,
        )
        return render(request, "article/createColumn.html", context)
