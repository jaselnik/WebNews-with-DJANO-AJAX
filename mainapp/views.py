from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Article, Category
from .mixins import CategoryListMixin
from .forms import CommentForm, RepostForm


class MainListView(ListView):

    template_name = 'mainapp/home.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainListView, self).get_context_data()
        context['hot_articles'] = self.model.objects.all().order_by('-id')[:4]
        context['popular_articles'] = self.model.objects.all().order_by('-id')[4:6]
        context['last_article_image'] = context['hot_articles'][3].image.url
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView, CategoryListMixin):

    template_name = 'mainapp/category_detail.html'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        context['category'] = self.get_object()
        context['articles'] = self.get_object().article_set.all()
        return context


class ArticleDetailView(DetailView, CategoryListMixin):

    template_name = 'mainapp/article_detail.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        context['article'] = self.get_object()
        context['article_comments'] = self.get_object().comments.all().order_by("-timestamp")
        context['comment_form'] = CommentForm()
        context['repost_form'] = RepostForm()
        marks_count = self.get_object().marks.all().values('status').annotate(count=Count('status'))
        likes_count = 0
        dislikes_count = 0
        for mark_count in marks_count:
            if mark_count['status'] in ('L', 'LIKE'):
                likes_count += mark_count['count']
            elif mark_count['status'] in ('D', 'DISLIKE'):
                dislikes_count += mark_count['count']
        context['article_likes'] = likes_count
        context['article_dislikes'] = dislikes_count
        context['article_reposts'] = self.get_object().reposts.all().count()
        return context


class HotArticleImageView(View):

    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('article_id')
        print(article_id)
        article = get_object_or_404(Article, id=article_id)
        data = {
            'article_image': article.image.url,
        }
        return JsonResponse(data)


class CommentSavingView(View):

    template_name = 'mainapp/article_detail.html'

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get('article_id')
        comment = self.request.POST.get('comment')
        article = Article.objects.get(pk=article_id)
        new_comment = article.comments.create(author=request.user, content=comment)
        data = [{
            'author': new_comment.author.get_full_name(),
            'comment': new_comment.content,
            'timestamp': new_comment.timestamp,
        }]
        return JsonResponse(data, safe=False)


class UserMarkedArticleView(View):

    template_name = 'mainapp/article_detail.html'

    def get(self, request, *args, **kwargs):
        mark = self.request.GET.get('mark')
        article_id = self.request.GET.get('article_id')
        article = Article.objects.get(pk=article_id)
        mark = mark.upper()
        if mark in ('D', 'L', 'DISLIKE', 'LIKE', ):
            new_mark = article.marks.create(author=request.user, status=mark[0])
            marks_count = article.marks.all().values('status').annotate(count=Count('status'))
            likes_count = 0
            dislikes_count = 0
            for mark_count in marks_count:
                if mark_count['status'] in ('L', 'LIKE'):
                    likes_count += mark_count['count']
                elif mark_count['status'] in ('D', 'DISLIKE'):
                    dislikes_count += mark_count['count']
            data = {
                'article_id': article_id,
                'article_likes': likes_count,
                'article_dislikes': dislikes_count,
                'status': 'OK',
            }
            return JsonResponse(data)


class UserRepostArticleView(View):

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get('article_id')
        comment = self.request.POST.get('comment')
        if not article_id:
            data = {
                'status': 'FATAL'
            }
            return JsonResponse(data)
        article = Article.objects.get(pk=article_id)
        if not article:
            data = {
                'status': 'FATAL'
            }
            return JsonResponse(data)
        new_repost = article.reposts.create(author=request.user, content=comment or '')
        article_reposts = article.reposts.all().count()
        data = {
            'article_reposts': article_reposts
        }
        return JsonResponse(data)
