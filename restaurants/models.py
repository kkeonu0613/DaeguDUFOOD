from django.contrib.auth.models import User
from django.db import models
from PIL import Image as PilImage

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='restaurants')
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    menu = models.TextField(blank=True, null=True)  # 메뉴 설명
    likes = models.IntegerField(default=0)  # 좋아요 수 필드 추가

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='reviews')  # 문자열로 참조
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Review by {self.author.username} on {self.restaurant}'

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # 이미지가 있는 경우 크기를 조정
        if self.image:
            img = PilImage.open(self.image)
            img.thumbnail((800, 800))
            img.save(self.image.path)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username} liked {self.restaurant.name}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')

    def __str__(self):
        return self.user.username
