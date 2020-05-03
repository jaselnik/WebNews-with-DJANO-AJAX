from django import forms
from django.utils.translation import gettext_lazy as _

from backend.models import Article, Comment


class CommentForm(forms.Form):

    comment = forms.CharField(
        label=_("Комментарий"),
        widget=forms.Textarea,
    )


class CommentEditForm(forms.ModelForm):
    content = forms.CharField(
        label=_("Комментарий"),
        widget=forms.Textarea,
    )

    class Meta:
        model = Comment
        fields = ("content",)


class RepostForm(forms.Form):
    repost_comment = forms.CharField(
        label=_("Заметка"),
        widget=forms.Textarea,
    )


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label=_("Название статьи"))
    content = forms.CharField(
        label=_("Текст статьи"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Добавть контент статьи...",
            },
        ),
    )
    image = forms.ImageField(label=_("Картинка статьи"))

    class Meta:
        model = Article
        fields = ("title", "content", "image")

    def save(self, user, category):
        article = super(ArticleForm, self).save(commit=False)
        article.author = user
        article.category = category
        article.save()

        return article


class ArticleEdit(forms.ModelForm):
    title = forms.CharField(label=_("Название статьи"))
    content = forms.CharField(
        label=_("Текст статьи"),
        widget=forms.Textarea,
    )
    image = forms.ImageField(label=_("Картинка статьи"))

    class Meta:
        model = Article
        fields = ("title", "content", "image")
