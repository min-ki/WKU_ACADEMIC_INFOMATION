from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post
from .forms import PostForm

def post_list(request):

    posts = Post.objects.all()

    return render(request, 'board/post_list.html', {
        'posts' : posts
    })


def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    return render(request, 'board/post_detail.html', {
        'post' : post
    })

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(form)
        if form.is_valid():  # 유효성 검사 수행
            post = form.save()
            messages.success(request, '새 포스팅을 저장했습니다.')
            return redirect(post)
    else:
        form = PostForm()
    return render(request, 'board/post_form.html', {
        'form': form,
    })
