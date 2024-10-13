"""
URL configuration for dufood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from restaurants.views import (
    main, category_view, restaurant_view, reviews_view,
    create_review, signup, login_view, logout_view,
    post_list, post_detail, post_create, post_edit, post_delete,
    like_post, comment_delete, comment_edit, comment_create, hot_posts, mypage, main_view, like_restaurant, edit_review, delete_review
)
from django.conf import settings
from django.conf.urls.static import static
from restaurants.views import hot_posts_view


urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', main, name='main'),
    path('', main_view, name='main'),  # 메인 페이지 URL
    path('category/<str:category_name>/', category_view, name='category'),
    path('restaurant/<int:restaurant_id>/', restaurant_view, name='restaurant_view'),
    path('restaurant/<int:restaurant_id>/reviews/', reviews_view, name='reviews'),
    path('restaurant/<int:restaurant_id>/create_review/', create_review, name='create_review'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('mypage/', mypage, name='mypage'),  # 마이페이지 URL 매핑
    path('post/', post_list, name='post_list'),  # 게시글 목록
    path('post/<int:post_id>/', post_detail, name='post_detail'),  # 게시글 상세 보기
    path('post/new/', post_create, name='post_create'),  # 새 게시글 작성
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'), # 게시글 수정
    path('post/<int:post_id>/delete/', post_delete, name='post_delete'), #게시글 삭제
    path('post/<int:post_id>/like/', like_post, name='like_post'),  # 게시글 추천
    path('post/<int:post_id>/comments/new/', comment_create, name='comment_create'), # 댓글 작성
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', comment_delete, name='comment_delete'),  # 댓글 삭제
    path('post/<int:post_id>/comment/<int:comment_id>/edit/', comment_edit, name='comment_edit'), # 댓글 수정
    path('hot-posts/', hot_posts, name='hot_posts'),
    path('hothot-posts/', hot_posts_view, name='hothot'),
    path('like/restaurant/<int:restaurant_id>/', like_restaurant, name='like_restaurant'),  # 식당 추천
    path('reviews/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('restaurant/<int:restaurant_id>/reviews/', reviews_view, name='reviews_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
