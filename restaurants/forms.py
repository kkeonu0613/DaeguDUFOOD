from django import forms
from .models import Review, Post, Comment, Profile

class ReviewForm(forms.ModelForm):
    # rating 필드 추가
    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    class Meta:
        model = Review
        fields = ['text', 'rating']  # rating 필드 추가
        labels = {
            'text': '리뷰',
            'rating': '평점'  # 별점 필드의 라벨 지정
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'author': forms.HiddenInput()  # author 필드 숨기기
        }

#게시판
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label='식당 이름')
    location = forms.CharField(required=False, label='위치')