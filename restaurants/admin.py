from django.contrib import admin
from restaurants.models import Category, Restaurant, Review, Post, Comment, Like

# Register your models here.
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Comment)

# Like 모델 등록
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'created_at')  # 원하는 필드를 리스트에 추가
