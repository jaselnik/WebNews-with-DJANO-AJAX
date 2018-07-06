from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Article, Category
from .mixins import CategoryListMixin


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
        return context


# not a perfect code, need your alternative view on it
def get_hot_image(request):
   article_id = request.GET.get('article_id')
   print(article_id)
   article = get_object_or_404(Article, id=article_id)
   data = {
       'article_image': article.image.url,
   }
   return JsonResponse(data)
