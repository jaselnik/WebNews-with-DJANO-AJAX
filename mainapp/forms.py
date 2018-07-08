from django import forms


class CommentForm(forms.Form):

    comment = forms.CharField(widget=forms.Textarea)


class RepostForm(forms.Form):

    repost_comment = forms.CharField(widget=forms.Textarea)
