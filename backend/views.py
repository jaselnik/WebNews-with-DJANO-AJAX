from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateformat import DateFormat, TimeFormat
from django.utils.decorators import method_decorator
from django.utils.formats import get_format
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from backend.forms import (
    ArticleEdit,
    ArticleForm,
    CommentEditForm,
    CommentForm,
    RepostForm,
)
from backend.mixins import CategoryListMixin
from backend.models import (
    Article,
    Category,
    Comment,
    Mark,
)


class MainListView(ListView):

    template_name = "frontend/home.html"
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainListView, self).get_context_data()
        context["hot_articles"] = self.model.objects.all().order_by("-id")[:4]
        context["popular_articles"] = self.model.objects.all().order_by("-id")[4:6]
        context["articles_count_enough"] = self.model.objects.all().count() > 3
        if context["articles_count_enough"]:
            context["last_article_image"] = context["hot_articles"][3].image.url
        context["categories"] = Category.objects.all()
        return context


class CategoryDetailView(DetailView, CategoryListMixin):

    template_name = "frontend/category_detail.html"
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        context["category"] = self.get_object()
        context["articles"] = self.get_object().article_set.all()
        context["article_form"] = ArticleForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST or None, request.FILES or None)
        import pdb; pdb.set_trace()
        if form.is_valid():
            user = request.user
            category = self.get_object()
            article = form.save(user, category)
            return redirect(article.get_absolute_url())
        context = super(CategoryDetailView, self).get_context_data()
        context["category"] = self.get_object()
        context["articles"] = self.get_object().article_set.all()
        context["article_form"] = form
        return context


class ArticleEditView(LoginRequiredMixin, TemplateView):

    template_name = "frontend/article_edit.html"

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs["slug"])
        if request.user != article.author:
            return Http404
        form = ArticleEdit(instance=article)
        path = request.path.split("/")
        args = {"form": form, "cat_slug": path[1], "slug": path[2]}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs["slug"])
        if request.user != article.author:
            return Http404
        form = ArticleEdit(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()

            return redirect(article.get_absolute_url())
        args = {"form": form}
        return render(request, self.template_name, args)


class CommentEditView(LoginRequiredMixin, TemplateView):

    template_name = "frontend/comment_edit.html"

    def get(self, request, *args, **kwargs):
        id_comment = kwargs["id"]
        slug = kwargs["slug"]
        comment = Comment.objects.get(id=kwargs["id"])
        if request.user != comment.author:
            return Http404
        form = CommentEditForm(instance=comment)
        args = {"form": form, "id_comment": id_comment, "slug": slug}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs["slug"])
        comment = Comment.objects.get(id=kwargs["id"])
        if request.user != comment.author:
            return Http404
        form = CommentEditForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(article.get_absolute_url())
        args = {"form": form}
        return render(request, self.template_name, args)


class ArticleDetailView(DetailView, CategoryListMixin):

    template_name = "frontend/article_detail.html"
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        path = self.request.path.split("/")
        context = super(ArticleDetailView, self).get_context_data()
        context["article"] = self.get_object()
        context["article_comments"] = (
            self.get_object().comments.all().order_by("-timestamp")
        )
        context["comment_form"] = CommentForm()
        context["repost_form"] = RepostForm()
        # context['article_reposts'] = self.get_object().reposts.all().count()  # NEED IMPROVE
        article_reposts = (
            self.get_object()
            .reposts.values("content")
            .all()
            .annotate(repost_count=Count("content_type"))
        )
        article_repost_count = 0
        for article_repost in article_reposts:
            article_repost_count += article_repost["repost_count"]
        context["article_reposts"] = article_repost_count
        context["cat_slug"] = path[1]
        context["slug"] = path[2]
        return context


class HotArticleImageView(View):
    def get(self, request, *args, **kwargs):
        article_id = request.GET.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        data = {"article_image": article.image.url}
        return JsonResponse(data)


class CommentSavingView(LoginRequiredMixin, View):

    template_name = "frontend/article_detail.html"

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get("article_id")
        comment = self.request.POST.get("comment")
        article = Article.objects.get(pk=article_id)
        new_comment = article.comments.create(author=request.user, content=comment)
        likes_count = new_comment.get_likes()
        dislikes_count = new_comment.get_dislikes()
        dt = datetime.now()
        df = DateFormat(dt)
        tf = TimeFormat(dt)
        new_comment_timestamp = (
            df.format(get_format("DATE_FORMAT"))
            + ", "
            + tf.format(get_format("TIME_FORMAT"))
        )
        data = [
            {
                "author": new_comment.author.get_full_name(),
                "comment": new_comment.content,
                "comment_id": new_comment.pk,
                "comment_likes": likes_count,
                "comment_dislikes": dislikes_count,
                "timestamp": new_comment_timestamp,
                "slug": article.slug,
            }
        ]
        return JsonResponse(data, safe=False)


class UserRepostArticleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get("article_id")
        comment = self.request.POST.get("comment")
        if not article_id:
            data = {"status": "FATAL"}
            return JsonResponse(data)
        article = Article.objects.get(pk=article_id)
        if not article:
            data = {"status": "FATAL"}
            return JsonResponse(data)
        article.reposts.create(author=request.user, content=comment or "")
        article_reposts = article.reposts.all().count()
        data = {"article_reposts": article_reposts}
        return JsonResponse(data)


class UserMarkedSomethingView(View):

    model = None
    model_obj = None
    model_mark = Mark

    def get(self, request, *args, **kwargs):
        author = request.user
        mark = self.request.GET.get("mark")
        obj_id = self.request.GET.get("obj_id")
        model_type = self.request.GET.get("model_type")
        ct = ContentType.objects.get(model=model_type)
        self.model = ct.model_class()
        self.model_obj = self.model.objects.get(pk=obj_id)

        mark = mark.upper()
        if mark in ("D", "L", "DISLIKE", "LIKE"):
            try:
                mark_obj = self.model_obj.marks.get(author=author)
                if (mark_obj.object_id == int(obj_id)) and (
                    mark_obj.content_type.model_class() == self.model
                ):
                    mark_obj.delete_or_switch(mark)
            except ObjectDoesNotExist:
                self.model_obj.marks.create(author=request.user, status=mark[0])
            likes_count = self.model_mark.get_related_likes(model_obj=self.model_obj)
            dislikes_count = self.model_mark.get_related_dislikes(
                model_obj=self.model_obj
            )
            data = {
                "obj_id": obj_id,
                "obj_likes": likes_count,
                "obj_dislikes": dislikes_count,
                "model_type": model_type,
                "status": "OK",
            }
            return JsonResponse(data)
