from django.views.generic.list import MultipleObjectMixin

<<<<<<< HEAD

=======
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
from .models import Category


class CategoryListMixin(MultipleObjectMixin):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['categories'] = Category.objects.all()
        return context
