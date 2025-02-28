"""posts_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import(
    post_list_and_create,
    load_post_data_view,
    like_unlike_post,
    post_detail,
    post_detail_data_view,
    delete_post,
    update_post
)

app_name = 'posts'

urlpatterns = [
    path('', post_list_and_create, name="main-board"),
    path('like-unlike/', like_unlike_post, name='like-unlike'),  # ✅ Sonunda `/` var
    path('<pk>/', post_detail, name ="post-detail" ),
    path('<pk>/update/', update_post, name ="post-update" ),
    path('<pk>/delete/', delete_post, name ="post-delete" ),
    

    path('data/<int:num_posts>/', load_post_data_view, name='posts-data'),
    path('<pk>/data/', post_detail_data_view, name='post-detail-data'),

]

