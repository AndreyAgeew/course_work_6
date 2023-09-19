from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import BlogPost


class BlogPostCreateView(CreateView, LoginRequiredMixin):
    model = BlogPost
    fields = ('title', 'content', 'preview_image')
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Добавить новую запись:'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogPostListView(ListView):
    model = BlogPost
    extra_context = {
        'title': 'Последнии записи в блоге:'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = BlogPost.objects.filter(is_published=True)
        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogPostUpdateView(UpdateView, LoginRequiredMixin):
    model = BlogPost
    fields = ('title', 'content', 'preview_image')
    extra_context = {
        'title': 'Редактировать запись:'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        title = self.kwargs.get('title')
        blog = get_object_or_404(BlogPost, title=title)
        if blog.owner != self.request.user and not self.request.user.is_staff:
            print("!!!!!")
            raise Http404
        return blog

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs.get('slug')])


class BlogPostDeleteView(DeleteView, LoginRequiredMixin):
    model = BlogPost
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Удаление записи:'
    }
