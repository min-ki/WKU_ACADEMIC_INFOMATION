from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post
from .forms import PostForm

def post_list(request):

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    
    posts = paginator.get_page(page)

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
        if form.is_valid():  # 유효성 검사 수행
            post = form.save()
            messages.success(request, '새 게시글을 저장했습니다.')
            return redirect(post)
    else:
        form = PostForm()
    return render(request, 'board/post_form.html', {
        'form': form,
    })

def post_edit(request, pk):    
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid(): 
            post = form.save()
            messages.success(request, '게시글을 수정했습니다.')
            return redirect(post)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_form.html', {
        'form': form,
    })

def post_delete(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.error(request, '게시글이 성공적으로 삭제되었습니다.')
    return redirect('board:list')
    
