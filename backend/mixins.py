from django.views.generic.list import MultipleObjectMixin

from .models import Category


class CategoryListMixin(MultipleObjectMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context["categories"] = Category.objects.all()
        return context
