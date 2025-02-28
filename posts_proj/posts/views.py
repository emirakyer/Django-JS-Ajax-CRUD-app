from django.shortcuts import render
from .models import Post
from django.http import JsonResponse
from .forms import PostForm
from profiles.models import Profile
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def post_list_and_create(request):
    form = PostForm(request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if form.is_valid():
            author = Profile.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
    context = {'form': form}
    return render(request, 'posts/main.html', context)

def post_detail(request, pk):
    obj = Post.objects.get(pk=pk)
    form = PostForm()

    context = {
        'obj': obj,
        'form': form
    }

    return render(request, 'posts/detail.html', context)

def load_post_data_view(request, num_posts):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        visible = 3
        upper = num_posts
        lower = upper - visible
        size = Post.objects.all().count()

        qs = Post.objects.all()[lower:upper]
        data = []
        for obj in qs:
            item = {
                'id': obj.id,
                'title': obj.title,
                'body': obj.body,
                'liked': obj.liked.filter(id=request.user.id).exists(),
                'count': obj.like_count,
                'author': obj.author.user.username
            }
            data.append(item)
        return JsonResponse({'data': data, 'size': size})

def post_detail_data_view(request, pk):
    obj = Post.objects.get(pk=pk)
    data = {
        'id': obj.id,
        'title': obj.title,
        'body': obj.body,
        'author': obj.author.user.username,
        'logged_in': request.user.username,
    }
    return JsonResponse({'data': data})


def like_unlike_post(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # ✅ AJAX isteği olup olmadığını kontrol et
        if request.method == "POST":
            pk = request.POST.get('pk')
            obj = get_object_or_404(Post, pk=pk)

            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User is not authenticated'}, status=401)  # ✅ Giriş kontrolü

            if request.user in obj.liked.all():
                obj.liked.remove(request.user)
                liked = False
            else:
                obj.liked.add(request.user)
                liked = True

            return JsonResponse({'liked': liked, 'count': obj.like_count})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)  # ✅ Yanlış istek formatı için hata döndür


def update_post(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
        new_title = request.POST.get('title')
        new_body = request.POST.get('body')
        obj.title = new_title
        obj.body = new_body
        obj.save()
        return JsonResponse({
            'title': new_title,
            'body': new_body,
        })

def delete_post(request, pk):
    obj = Post.objects.get(pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
        obj.delete()
        return JsonResponse({})