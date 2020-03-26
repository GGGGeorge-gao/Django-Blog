from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from my_blog.models import ArticlePost
from .forms import CommentForm
from .models import Comment


# Create your views here.


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.article = article

            if parent_comment_id:
                parent_comment = Comment.objects.get_queryset(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect("my_blog:article_detail", article_id)
        elif not comment_form['body']:
            return HttpResponse("评论内容不能为空!")
        else:
            return HttpResponse("请勿输入非法字符")

    elif request.method == 'GET':
        comment_form = CommentForm()
        context = dict(
            comment_form=comment_form,
            article_id=article_id,
            parent_comment_id=parent_comment_id,
        )
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("仅接受GET/POST请求")


@login_required(login_url='/userprofile/login/')
def comment_delete(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        article_id = comment.article_id
        if request.user.id == comment.user.id:
            comment.delete()
            return redirect("my_blog:article_detail", article_id)
        else:
            return HttpResponse("抱歉！您没有删除操作的权限。")
    else:
        return HttpResponse("该操作仅接受POST请求。")