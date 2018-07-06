from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Article, Category
from .mixins import CategoryListMixin
from .forms import CommentForm


class MainListView(ListView):

    template_name = 'home.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainListView, self).get_context_data()
        context['hot_articles'] = self.model.objects.all().order_by('-id')[:4]
        context['popular_articles'] = self.model.objects.all().order_by('-id')[4:6]
        context['last_article_image'] = context['hot_articles'][3].image.url
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView, CategoryListMixin):

    template_name = 'category_detail.html'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        context['category'] = self.get_object()
        context['articles'] = self.get_object().article_set.all()
        return context


class ArticleDetailView(DetailView, CategoryListMixin):

    template_name = 'article_detail.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        context['article'] = self.get_object()
        context['article_comments'] = self.get_object().comments.all().order_by("-timestamp")
        context['form'] = CommentForm()
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

    template_name = 'article_detail.html'

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get('article_id')
        comment = self.request.POST.get('comment');
        article = Article.objects.get(id=article_id)
        new_comment = article.comments
        new_comment = article.comments.create(author=request.user, content=comment)
        data = [{
            'author': new_comment.author.username,
            'comment': new_comment.content,
            'timestamp': new_comment.timestamp,
        }]
        return JsonResponse(data, safe=False)
