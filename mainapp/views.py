from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.utils.dateformat import DateFormat
from django.utils.dateformat import TimeFormat
from django.utils.formats import get_format
from django.shortcuts import redirect, reverse


from .models import Article, Category, Repost, Mark
from .mixins import CategoryListMixin
from .forms import CommentForm, RepostForm, ArticleForm

from datetime import datetime


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
        context['article_form'] = ArticleForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = request.user
            category = self.get_object()
            article = form.save(user, category)
            return redirect(article.get_absolute_url())
        else:
            print('_$_$_$_$_$_$_')
        context = super(CategoryDetailView, self).get_context_data()
        context['category'] = self.get_object()
        context['articles'] = self.get_object().article_set.all()
        context['article_form'] = form
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
        likes_count = Mark.get_related_likes(model_obj=self.get_object())
        dislikes_count = Mark.get_related_dislikes(model_obj=self.get_object())
        for mark_count in marks_count:
            if mark_count['status'] in ('L', 'LIKE'):
                likes_count += mark_count['count']
            elif mark_count['status'] in ('D', 'DISLIKE'):
                dislikes_count += mark_count['count']
        context['article_likes'] = likes_count
        context['article_dislikes'] = dislikes_count
        context['article_reposts'] = self.get_object().reposts.all().count()  # NEED IMPROVE
        return context


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'image')


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
        likes_count = new_comment.get_likes()
        dislikes_count = new_comment.get_dislikes()
        dt = datetime.now()
        df = DateFormat(dt)
        tf = TimeFormat(dt)
        new_comment_timestamp = df.format(get_format('DATE_FORMAT')) + ', '\
                                + tf.format(get_format('TIME_FORMAT'))
        data = [{
            'author': new_comment.author.get_full_name(),
            'comment': new_comment.content,
            'comment_id': new_comment.pk,
            'comment_likes': likes_count,
            'comment_dislikes': dislikes_count,
            'timestamp': new_comment_timestamp,
        }]
        return JsonResponse(data, safe=False)


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


class UserMarkedSomethingView(View):

    model = None
    model_obj = None
    model_mark = Mark

    def get(self, request, *args, **kwargs):
        author = request.user
        mark = self.request.GET.get('mark')
        obj_id = self.request.GET.get('obj_id')
        model_type = self.request.GET.get('model_type')
        ct = ContentType.objects.get(model=model_type)
        self.model = ct.model_class()
        self.model_obj = self.model.objects.get(pk=obj_id)

        mark = mark.upper()
        if mark in ('D', 'L', 'DISLIKE', 'LIKE', ):
            try:
                mark_obj = self.model_obj.marks.get(author=author)
                if (mark_obj.object_id == int(obj_id)) and (mark_obj.content_type.model_class() == self.model):
                    print(mark_obj.delete_or_switch(mark))
            except ObjectDoesNotExist:
                new_mark = self.model_obj.marks.create(author=request.user, status=mark[0])
            likes_count = self.model_mark.get_related_likes(model_obj=self.model_obj)
            dislikes_count = self.model_mark.get_related_dislikes(model_obj=self.model_obj)
            data = {
                'obj_id': obj_id,
                'obj_likes': likes_count,
                'obj_dislikes': dislikes_count,
                'model_type': model_type,
                'status': 'OK',
            }
            return JsonResponse(data)


# '%d %b, %Y'
