from distutils.command.upload import upload
from django.db import models
from shop.models import Product
from django.template.defaultfilters import slugify

# Create your models here.
class Cart(models.Model) :
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta :
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self) :
        return self.cart_id

class CartItem(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default = True)

    class Meta :
        db_table = 'CartItem'

    def sub_total(self) :
        return self.product.price * self.quantity
    
    def __str__(self) :
        return self.product

class Post(models.Model):
    realname = models.CharField(max_length=10)
    artist_name = models.CharField(max_length=30)
    team = models.CharField(max_length=64)
    email = models.EmailField()
    artist_intro = models.TextField(max_length=300)
    post_intro = models.TextField(max_length=300)
    post_plan = models.TextField()
    # 전시 장소 추가 필요

    def __str__(self):
        return self.artist_name

    class Meta:
        db_table = 'post'
        verbose_name = 'post'
        verbose_name_plural = 'post'

def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

# 다중 이미지 삽입을 위한 모델
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    image = models.ImageField(default='media/post/default_image.jpg', upload_to='post', blank=True, null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return str(self.post)