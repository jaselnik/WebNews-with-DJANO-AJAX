from django.urls import path, re_path

from .views import (
    ArticleDetailView,
    ArticleEditView,
    CategoryDetailView,
    CommentEditView,
    CommentSavingView,
    HotArticleImageView,
    MainListView,
    UserMarkedSomethingView,
    UserRepostArticleView,
)

app_name = "main"

urlpatterns = [
    path("add_comment/", CommentSavingView.as_view(), name="add-comment"),
    path("hot-image-view/", HotArticleImageView.as_view(), name="get-hot-image"),
    path(
        "user-repost-article/",
        UserRepostArticleView.as_view(),
        name="user-repost-article",
    ),
    path(
        "user-marked-something/",
        UserMarkedSomethingView.as_view(),
        name="user-marked-something",
    ),
    path("", MainListView.as_view(), name="home"),
    re_path(
        r"^(?P<slug>[-\w]+)/$", CategoryDetailView.as_view(), name="category-detail"
    ),
    re_path(
        r"^comment/(?P<slug>[-\w]+)/(?P<id>\d+)/edit$",
        CommentEditView.as_view(),
        name="comment-edit",
    ),
    re_path(
        r"^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    re_path(
        r"^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/edit$",
        ArticleEditView.as_view(),
        name="article-edit",
    ),
    re_path(
        r"^(?P<cat_slug>[-\w]+)/(?P<slug>[-\w]+)/$",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
]
