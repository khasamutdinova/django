# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404
# from django.views.generic import ListView, CreateView, UpdateView


# class ListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'

# class CreateView(CreateView):
#     form_class = PostForm
#     template_name = 'blog/post_new.html'
#     context_object_name = 'post'
#     PermissionRequired = ('post_new')

#     def form_valid(self, form):
#        post = form.save(commit=False)
#        post.published_date = timezone.now()
#        post.save()
#        return redirect ('post_detail', pk=post.pk)
    
# class PostEdit(UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'blog/post/edit.html'

#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.author = self.request.user
#         post.published = self.request.user
#         post.save()
#         return redirect('post_detail', pk=post.pk)





def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# @login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})