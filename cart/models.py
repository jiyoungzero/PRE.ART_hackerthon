from distutils.command.upload import upload
from django.db import models
from shop.models import Product
from django.template.defaultfilters import slugify
from accounts.models import Member

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
    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    like_user_set = models.ManyToManyField(Member, blank=True, related_name='likes_user_set', through='Like')

    @property
    def like_count(self):
        return self.like_user_set.count()

    def __str__(self):
        return self.artist_name

    class Meta:
        db_table = 'post'
        verbose_name = 'post'
        verbose_name_plural = 'post'


class CartItem(models.Model) :
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default = True)

    class Meta :
        db_table = 'CartItem'

    def sub_total(self) :
        return self.product.price * self.quantity
    
    def __str__(self) :
        return self.product

# 다중 이미지 삽입을 위한 모델
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="image")
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)

class Like(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'))