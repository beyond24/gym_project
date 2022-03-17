import markdown
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from app01.models import ArticlePost, ArticleColumn, Comment, User
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm

def article_list(request):
    articles = ArticlePost.objects.all()
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    if column is not None and column.isdigit():
        articles = articles.filter(column=column)
    if tag and tag != 'None':
        articles = articles.filter(tags__name__in=[tag])

    page_object = Pagination(request, articles, page_size=5, )

    hot_article = ArticlePost.objects.all().order_by('-total_views').values('id','title', 'total_views')[:10]

    content = {
        'articles': page_object.page_queryset,
        'page_string': page_object.html(),
        'hot_article': hot_article,


    }

    return render(request, 'article_list.html', content)

class CommentModelForm(BootstrapModelForm):
    class Meta:
        model = Comment
        fields = ['body']


def article_detail(request, nid):
    article = ArticlePost.objects.get(id=nid)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])
    comments = Comment.objects.filter(article=nid)
    comment_form = CommentModelForm
    content = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'article_detail.html', content)




def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # 返回对象添加额外数据后在储存
            new_comment.article = article
            print(request.session)
            user_obj = User.objects.get(id=request.session['info']['id'])
            new_comment.user = user_obj
            new_comment.save()
        return redirect(article)

    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")