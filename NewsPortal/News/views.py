from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'data'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['time_now'] = datetime.utcnow()
        return contex


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['time_now'] = datetime.utcnow()
        return contex
