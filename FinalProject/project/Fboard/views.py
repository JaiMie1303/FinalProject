from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ReplyForm
from .models import *


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(DeleteView):
    queryset = Post.objects.all()
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def reply(request, pk):
    author, status = Author.objects.get_or_create(name=request.user)
    post = Post.objects.get(id=pk)
    form = ReplyForm()
    context = {'post': post,
               'form': form,
               'author': author
               }
    return render(request, 'reply.html', context)


def replied(request, pk):
    content = request.POST['content']
    author = Author.objects.get(name=request.user)
    post = Post.objects.get(id=pk)
    Reply.objects.create(author=author, post=post, content=content)
    return redirect('/')


class PersonalAreaView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'personal_area.html'
    context_object_name = 'replies'

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        author, created = Author.objects.get_or_create(name=user)
        queryset = Reply.objects.filter(author=author).order_by('-created_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['current_user'] = Author.objects.get(name=self.request.user)
        return context


class SortedByPostView(ListView):
    model = Reply
    template_name = 'replies_by_post.html'
    ordering = '-created_date'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = Reply.objects.filter(post=Post.objects.get(id=self.kwargs['post_id']))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['this_post'] = Post.objects.get(id=self.kwargs['post_id'])
        return context


class ReplyDetailView(DetailView):
    model = Reply
    ordering = '-created_date'
    template_name = 'reply_detail.html'
    context_object_name = 'reply'


class ReplyDeleteView(DeleteView):
    model = Reply
    success_url = reverse_lazy('personal_area')
    template_name = 'reply_delete.html'


def reply_approve(request, pk):
    obj = Reply.objects.get(id=pk)
    obj.approved = True
    obj.save()
    return redirect('/personal')


@login_required
def subscribe(request):
    obj = Author.objects.get(name=request.user)
    obj.is_subscriber = True
    obj.save()
    return redirect('/personal')


@login_required
def unsubscribe(request):
    obj = Author.objects.get(name=request.user)
    obj.is_subscriber = False
    obj.save()
    return redirect('/personal')







