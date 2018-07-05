from django.urls import path, re_path

from .views import MainListView, CategoryDetailView


app_name = 'main'

urlpatterns = [
    path('', MainListView.as_view(), name='home'),
    re_path('^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category-detail')
]
