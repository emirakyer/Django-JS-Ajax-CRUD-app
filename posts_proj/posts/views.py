from django.shortcuts import render
from .models import Post
from django.http import JsonResponse

# Create your views here.

def post_list_and_create(request):
    qs = Post.objects.all()
    return render(request, 'posts/main.html', {'qs':qs})

def load_post_data_view(request, num_posts):
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


from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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

def hello_world_view(request):
    return JsonResponse({'text': 'hello world'})


