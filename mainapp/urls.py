from django.urls import path, re_path

from .views import (
    MainListView, CategoryDetailView, ArticleDetailView, HotArticleImageView, CommentSavingView
)


app_name = 'main'

urlpatterns = [
    path('add_comment/', CommentSavingView.as_view(), name='add-comment'),
    path('', MainListView.as_view(), name='home'),
    re_path('^(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category-detail'),
    re_path('^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
    path('hot-image-view/', HotArticleImageView.as_view(), name='get-hot-image'),
]
