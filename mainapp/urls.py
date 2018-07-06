from django.urls import path, re_path

from .views import MainListView, CategoryDetailView, ArticleDetailView, get_hot_image


app_name = 'main'

urlpatterns = [
    path('', MainListView.as_view(), name='home'),
    re_path('^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category-detail'),
    re_path('^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
    path('hot-image-view/', get_hot_image, name='get-hot-image')
]
