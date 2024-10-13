from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, PostForm, CommentForm, ProfilePictureForm, RestaurantSearchForm 
from .models import Category, Restaurant, Review, Post, Comment, Like, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.db.models import Avg
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
import random
from django.db.models import Q 
# Create your views here.

def main(request):
    return render(request, 'main.html')

def main_view(request):
    form = RestaurantSearchForm(request.GET or None)

    # 기본적으로 모든 식당 가져오기
    restaurants = Restaurant.objects.all().order_by('?')
    search_query = ""
    selected_categories = request.GET.getlist('categories')  # 체크된 카테고리 목록

        # 검색어와 위치 처리
    if form.is_valid():
        name = form.cleaned_data.get('name')  # 사용자가 입력한 식당 또는 카테고리 이름
        location = form.cleaned_data.get('location')

        if name:  # 사용자가 입력한 값으로 필터링
            search_query = name
            # 이름 또는 카테고리로 필터링
            restaurants = restaurants.filter(
                Q(name__icontains=name) | Q(category__name__icontains=name)
            )

        if location:
            search_query = location
            restaurants = restaurants.filter(location__icontains=location)

    # 카테고리 필터링
    if selected_categories:
        selected_categories = [cat for cat in selected_categories if cat.isdigit()]
        if selected_categories:
            restaurants = restaurants.filter(category__id__in=selected_categories)

    # 랜덤 식당 처리
    random_restaurant = None
    if request.GET.get('random'):
        if restaurants.exists():  # 필터링된 식당이 있을 경우
            random_restaurant = random.choice(list(restaurants))

    # 랜덤 식당을 restaurants에 추가
    if random_restaurant:
        restaurants = [random_restaurant]  # 랜덤 식당만 리스트로 설정

    # 평균 평점과 첫 번째 리뷰 내용 추가
    for restaurant in restaurants:
        restaurant.average_rating = Review.objects.filter(restaurant=restaurant).aggregate(Avg('rating'))['rating__avg'] or 0.0
        first_review = Review.objects.filter(restaurant=restaurant).first()
        restaurant.first_review_text = first_review.text if first_review else "리뷰가 없습니다."

    # 페이지네이션 추가
    paginator = Paginator(restaurants, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 페이지 번호 리스트 생성
    total_pages = paginator.num_pages
    current_page = page_obj.number

    # 페이지 범위 설정 - 현재 페이지를 기준으로 4개씩 보여줌
    start_page = max(current_page - 4, 1)
    end_page = min(current_page + 5, total_pages)
    page_range = list(range(start_page, end_page + 1))

    # URL 쿼리 문자열 생성
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 페이지 번호는 제외
    query_string = query_params.urlencode()

    # URL 쿼리 문자열 생성
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 페이지 번호는 제외
    query_string = query_params.urlencode()

    return render(request, 'main.html', {
        'restaurants': page_obj,
        'form': form,
        'search_query': search_query,
        'random_restaurant': random_restaurant,
        'categories': Category.objects.all(),
        'selected_categories': selected_categories,
        'query_string': query_string,  # 쿼리 문자열을 템플릿에 전달
        'page_range': page_range,  # 페이지 번호 리스트 전달
        'current_page': page_number,  # 현재 페이지 전달
    })


def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    restaurants = category.restaurants.all()

    # 각 식당에 대한 평균 평점, 첫 번째 리뷰 내용, 위치 추가
    for restaurant in restaurants:
        # 평균 평점 계산
        restaurant.average_rating = Review.objects.filter(restaurant=restaurant).aggregate(Avg('rating'))['rating__avg'] or 0.0

        # 첫 번째 리뷰 내용 가져오기
        first_review = Review.objects.filter(restaurant=restaurant).first()
        restaurant.first_review_text = first_review.text if first_review else "리뷰가 없습니다."

    # 사용자 좋아요 상태 확인
    user_liked_restaurants = set()
    if request.user.is_authenticated:
        user_liked_restaurants = set(Like.objects.filter(user=request.user).values_list('restaurant_id', flat=True))

    return render(request, 'category.html', {
        'category': category,
        'restaurants': restaurants,
        'user_liked_restaurants': user_liked_restaurants,  # 사용자 좋아요 상태 추가
    })


@login_required(login_url=reverse_lazy('login'))
def create_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.author = request.user  # 현재 로그인한 사용자를 리뷰의 작성자로 설정
            review.save()
            # 리뷰 작성 후 해당 식당의 리뷰 페이지로 리다이렉트
            return HttpResponseRedirect(reverse('reviews', kwargs={'restaurant_id': restaurant_id}))
    else:
        form = ReviewForm()
    # 리뷰 작성 페이지로 이동
    return render(request, 'create_review.html', {'form': form, 'restaurant': restaurant})

def reviews_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = restaurant.reviews.all()
    return render(request, 'review.html', {'restaurant': restaurant, 'reviews': reviews})

def get_menu_content(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_content = restaurant.menu
    return JsonResponse({'menu_content': menu_content})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')  # 회원가입 후 메인 페이지로 리다이렉트
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 만약 로그인 이전에 리뷰 작성 페이지로 이동하려는 요청이 있었다면 해당 페이지로 이동하고,
            # 그렇지 않으면 'main'으로 이동합니다.
            next_url = request.GET.get('next', 'main')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main')

def restaurant_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    reviews = restaurant.reviews.all()

    # 리뷰가 있을 때만 평균 별점을 계산합니다.
    average_rating = None
    if reviews.exists():
        average_rating_dict = reviews.aggregate(Avg('rating'))
        average_rating = average_rating_dict['rating__avg'] or 0.0

    # 현재 사용자가 좋아요를 눌렀는지 확인
    user_liked = Like.objects.filter(user=request.user, restaurant=restaurant).exists() if request.user.is_authenticated else False

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'average_rating': average_rating,
        'user_liked': user_liked,  # 사용자가 좋아요를 눌렀는지 상태 추가
    }
    return render(request, 'restaurant.html', context)


#<---------------------자유게시판--------------------------->
def post_list(request):
    query = request.GET.get('q', '')  # 검색어 가져오기
    search_by = request.GET.get('search_by', 'title')  # 검색 기준 가져오기

    # 검색 조건에 따라 게시글 필터링
    if query:
        if search_by == 'title':
            posts = Post.objects.filter(title__icontains=query)  # 제목에서 검색
        elif search_by == 'content':
            posts = Post.objects.filter(content__icontains=query)  # 내용에서 검색
        elif search_by == 'author':
            posts = Post.objects.filter(author__username__icontains=query)  # 작성자에서 검색
    else:
        posts = Post.objects.all()  # 모든 게시글 가져오기

    # 최신순으로 정렬
    posts = posts.order_by('-created_at')

    # 페이지네이션 적용
    paginator = Paginator(posts, 10)  # 한 페이지에 10개씩 보여주기
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'page_obj': page_obj})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1  # 조회수 증가
    post.save()  # 변경 사항 저장

    # 댓글을 최신순으로 정렬하여 가져오기
    comments = post.comments.order_by('-created_at')  # 최신순으로 정렬

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # 이미지 파일 처리

        if request.user.is_authenticated:
            post = Post(author=request.user, title=title, content=content, image=image)  # 이미지 저장
            post.save()
            return redirect('post_list')

    return render(request, 'post_form.html')

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 게시글 작성자와 현재 사용자 비교
    if post.author != request.user:
        return redirect('post_list')  # 권한이 없으면 목록으로 리다이렉트

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)  # 수정한 게시글 상세 페이지로 리다이렉트
    else:
        form = PostForm(instance=post)  # 기존 게시글 정보로 폼 초기화

    return render(request, 'post_form.html', {
        'form': form,
        'post': post,  # 게시글 정보를 템플릿에 전달
        'is_edit': True  # 수정 모드임을 알리는 플래그
    })

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('post_list')  # 권한이 없으면 목록으로 리다이렉트

    if request.method == "POST":
        post.delete()
        return redirect('post_list')  # 삭제 후 목록 페이지로 리다이렉트

    return render(request, 'post_confirm_delete.html', {'post': post})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if not Like.objects.filter(user=request.user, post=post).exists():
                Like.objects.create(user=request.user, post=post)
                post.likes += 1
                post.save()
                return JsonResponse({'likes': post.likes})  # JSON 응답
    return JsonResponse({'likes': post.likes}, status=400)  # 오류 응답

def comment_create(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # 예시로 현재 사용자 설정
            comment.save()
            return redirect('post_detail', post_id=post.id)  # 댓글 등록 후 포스트 상세 페이지로 리다이렉트
    return redirect('post_list')  # 잘못된 접근 시 포스트 목록으로 리다이렉트

@login_required
def comment_edit(request, post_id, comment_id):
    # 댓글 객체 가져오기
    comment = get_object_or_404(Comment, pk=comment_id)

    # 댓글 작성자인지 확인
    if request.user != comment.author:
        return HttpResponseForbidden("수정 권한이 없습니다.")  # 수정 권한이 없다면 403 에러 리턴

    if request.method == "POST":
        comment.content = request.POST.get('content')
        comment.save()
        return redirect('post_detail', post_id=post_id)

    return render(request, 'post_detail.html', {'comment': comment, 'post_id': post_id})


@login_required
def comment_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)  # 게시글 가져오기
    comment = get_object_or_404(Comment, pk=comment_id)  # 댓글 가져오기

    # 댓글 작성자 확인
    if comment.author != request.user:
        return redirect('post_detail', post_id=post_id)  # 권한이 없으면 게시글 상세로 리다이렉트

    if request.method == "POST":
        comment.delete()  # 댓글 삭제
        return redirect('post_detail', post_id=post_id)  # 삭제 후 게시글 상세 페이지로 리다이렉트

    return render(request, 'comment_confirm_delete.html', {'comment': comment, 'post': post})  # 삭제 확인 페이지

def hot_posts(request):
    top_posts = Post.objects.order_by('-likes')[:3]  # 추천수가 높은 게시글 3개
    recommended_posts = Post.objects.filter(likes__gte=20).order_by('-created_at')  # 추천수가 20 이상인 게시글
    return render(request, 'hot_posts.html', {
        'top_posts': top_posts,
        'recommended_posts': recommended_posts,
    })

def hot_posts_view(request):
    query = request.GET.get('q', '')  # 검색어 가져오기
    search_by = request.GET.get('search_type', 'title')  # 검색 기준 가져오기

    # 추천수가 20개 이상인 게시글 중 최신 3개
    top_posts = Post.objects.filter(likes__gte=20).order_by('-created_at')[:3]
    
    # 추천수가 20 이상인 게시글, 최신순으로 정렬
    recommended_posts = Post.objects.filter(likes__gte=20).order_by('-created_at')
    # 검색 조건에 따라 게시글 필터링
    if query:
        if search_by == 'title':
            recommended_posts = recommended_posts.filter(title__icontains=query)  # 제목에서 검색
        elif search_by == 'content':
            recommended_posts = recommended_posts.filter(content__icontains=query)  # 내용에서 검색
        elif search_by == 'author':
            recommended_posts = recommended_posts.filter(author__username__icontains=query)  # 작성자에서 검색

    top_posts = recommended_posts.order_by('-likes')[:3]  # 추천수가 가장 높은 3개의 게시글

    context = {
        'top_posts': top_posts,
        'recommended_posts': recommended_posts,
        'query': query,  # 검색어 추가
        'search_type': search_by,  # 검색 기준 추가
    }
    
    return render(request, 'hot_posts.html', context)

@login_required
def mypage(request):
    # 사용자 프로필 가져오기
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'password_change' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
                return redirect('mypage')
            else:
                messages.error(request, '비밀번호 변경에 실패했습니다. 다시 시도해 주세요.')

        elif 'profile_picture' in request.POST:
            form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, '프로필 사진이 성공적으로 변경되었습니다.')
                return redirect('mypage')
            else:
                messages.error(request, '프로필 사진 변경에 실패했습니다. 다시 시도해 주세요.')

        elif 'delete_picture' in request.POST:
            if profile.profile_picture.name != 'Profile_pictures/default.jpg':
                profile.profile_picture.delete()  # 기존 사진 삭제
                profile.profile_picture = 'Profile_pictures/default.jpg'  # 기본 사진으로 설정
                profile.save()
                messages.success(request, '프로필 사진이 삭제되었습니다.')
            else:
                messages.error(request, '기본 프로필 사진은 삭제할 수 없습니다.')
            return redirect('mypage')

    # 비밀번호 변경 및 프로필 사진 변경 폼
    password_form = PasswordChangeForm(request.user)
    profile_picture_form = ProfilePictureForm(instance=profile)

    # 현재 사용자가 작성한 게시글과 리뷰를 가져옵니다.
    user_posts = Post.objects.filter(author=request.user)  # 현재 사용자가 작성한 게시글 필터링
    user_reviews = Review.objects.filter(author=request.user)  # 현재 사용자가 작성한 리뷰 필터링

    # 사용자가 좋아요를 누른 가게 목록 가져오기
    liked_restaurants = Restaurant.objects.filter(like__user=request.user)

    return render(request, 'mypage.html', {
        'password_form': password_form,
        'profile_picture_form': profile_picture_form,
        'reviews': user_reviews,  # 사용자 작성 리뷰를 넘깁니다.
        'posts': user_posts,  # 사용자 작성 게시글을 넘깁니다.
        'profile': profile,
        'liked_restaurants': liked_restaurants,  # 좋아요를 누른 가게 목록
    })
    
@login_required
def like_restaurant(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # 좋아요 상태 확인
        like, created = Like.objects.get_or_create(user=request.user, restaurant=restaurant)

        if created:
            # 좋아요 추가
            restaurant.likes += 1  # 좋아요 수 증가
            restaurant.save()  # 변경 사항 저장
            response = {'likes': True}
        else:
            # 좋아요 제거
            if restaurant.likes > 0:  # 좋아요 수가 0보다 클 때만 감소
                like.delete()
                restaurant.likes -= 1  # 좋아요 수 감소
                restaurant.save()  # 변경 사항 저장
                response = {'likes': False}
            else:
                response = {'error': '좋아요 수는 0 이하로 내려갈 수 없습니다.'}

        return JsonResponse(response)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 리뷰 수정
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews_view', restaurant_id=review.restaurant.id)  # 수정 후 리뷰 페이지로 리다이렉트
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})

# 리뷰 삭제
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    restaurant_id = review.restaurant.id  # 삭제할 리뷰의 식당 ID 저장
    review.delete()
    return redirect('reviews_view', restaurant_id=restaurant_id)  # 삭제 후 리뷰 페이지로 리다이렉트