from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article, Category


class MainListView(ListView):

    template_name = 'home.html'
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainListView, self).get_context_data()
        context['articles'] = self.model.objects.all()
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):

    template_name = 'category_detail.html'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        context['categories'] = self.model.objects.all()
        context['category'] = self.get_object()
        return context
