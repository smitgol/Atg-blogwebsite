from django.shortcuts import render, redirect
from .form import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Blog

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

class PostDetailview(LoginRequiredMixin, DetailView):
    model = Blog

class PostListView(ListView):
    def get_queryset(self):
        set = Blog.objects.filter(user=self.request.user)
        return set
    template_name = 'bloghome.html'
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'description', 'image', 'post_mode']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'description', 'image', 'post_mode']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/blog'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

class PostSearchList(ListView):
    template_name = 'blogapp/blog_search.html'
    model = Blog
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query, post_mode="Public")
        else:
            object_list = self.model.objects.none()
        return object_list