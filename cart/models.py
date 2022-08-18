from distutils.command.upload import upload
from django.db import models
from shop.models import Category
from django.template.defaultfilters import slugify
from accounts.models import Member
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model) :
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta :
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self) :
        return self.cart_id

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    realname = models.CharField(max_length=10)
    artist_name = models.CharField(max_length=30)
    team = models.CharField(max_length=64)
    email = models.EmailField()
    artist_intro = models.TextField(max_length=300)
    post_intro = models.TextField(max_length=300)
    post_plan = models.TextField()
    ok = models.BooleanField(default=False)
    tag = models.ManyToManyField('tag.Tag', verbose_name = "태그")
    post_price = models.DecimalField(max_digits=10, decimal_places=0)
    post_place = models.TextField()
    startday = models.DateField(null=True)
    endday = models.DateField(null=True)

    # 좋아요 추가
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    like_user_set = models.ManyToManyField(User, blank=True, related_name='likes_user_set', through='Like')

    # product 모델 합치기
    post_name = models.CharField(max_length=100, null=True, blank=True) # 전시회 이름
    main_image = models.ImageField(upload_to='post_image/', blank=True) # 전시회 메인 사진
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    # slug = models.SlugField(max_length=250, unique=True, null=True)

    # def get_url(self):
    #     return reverse('shop:PostDetail', args=[self.category.slug, self.slug])

    @property
    def like_count(self):
        return self.like_user_set.count()

    def __str__(self):
        return self.post_name

    class Meta:
        db_table = 'post'
        verbose_name = 'post'
        verbose_name_plural = 'post'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =(('user', 'post'))

class CartItem(models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default = True)

    class Meta :
        db_table = 'CartItem'

    def sub_total(self) :
        return self.post.post_price * self.quantity
    
    def __str__(self) :
        return self.post

# 다중 이미지 삽입을 위한 모델
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="image")
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)