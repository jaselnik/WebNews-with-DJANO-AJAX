from django.urls import path, re_path

<<<<<<< HEAD

from .views import (
    MainListView, CategoryDetailView, ArticleDetailView,
    HotArticleImageView, CommentSavingView,
    UserRepostArticleView, UserMarkedSomethingView,
    ArticleEditView, CommentEditView
=======
from .views import (
    MainListView, CategoryDetailView, ArticleDetailView,
    HotArticleImageView, CommentSavingView,
    UserRepostArticleView, UserMarkedSomethingView
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
)


app_name = 'main'

urlpatterns = [
    path('add_comment/', CommentSavingView.as_view(), name='add-comment'),
    path('hot-image-view/', HotArticleImageView.as_view(), name='get-hot-image'),
    path('user-repost-article/', UserRepostArticleView.as_view(), name='user-repost-article'),
    path('user-marked-something/', UserMarkedSomethingView.as_view(), name='user-marked-something'),
    path('', MainListView.as_view(), name='home'),
    re_path('^(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category-detail'),
<<<<<<< HEAD
    re_path('^comment/(?P<slug>[-\w]+)/(?P<id>\d+)/edit$', CommentEditView.as_view(), name='comment-edit'),
    re_path('^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
    re_path('^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/edit$', ArticleEditView.as_view(), name='article-edit'),
=======
    # path('article/create/', ArticleCreateView.as_view(), name='article-create'),
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
    re_path('^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
]
