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
    id = models.AutoField(primary_key=True)
    realname = models.CharField(max_length=10)
    artist_name = models.CharField(max_length=30)
    team = models.CharField(max_length=64)
    email = models.EmailField()
    artist_intro = models.TextField(max_length=300)
    post_intro = models.TextField(max_length=300)
    post_plan = models.TextField()
    

    ok = models.BooleanField(default=False)

    # option_choices = [
    #     ('승인 대기', '승인 대기'),
    #     ('승인 완료', '승인 완료'),
    # ]
    # option = models.CharField(max_length=10, choices = option_choices, default='승인 대기')

    # post_img = models.ImageField(upload_to="cart/post_img")
    post_price = models.DecimalField(max_digits=10, decimal_places=0)
    post_place = models.TextField()
    startday = models.DateField(null=True)
    endday = models.DateField(null=True)
    # 전시 장소 일단 form 불러와야 할 것 같아서 추가해뒀습니다.

    # 전시 장소,목표가격,전시명 추가 필요
    non_free = "# 유료"
    free = "# 무료"
    popart = "# 팝아트"
    TAG_CHOICES = [
    ('non_free', '# 유료'),
    ('free', '# 무료'),
    ('popart', '# 팝아트'),
    ] 
    
    post_tag = models.CharField(max_length=300, choices= TAG_CHOICES)


    def __str__(self):
        return self.artist_name

    class Meta:
        db_table = 'post'
        verbose_name = 'post'
        verbose_name_plural = 'post'

# 다중 이미지 삽입을 위한 모델
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="image")
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)


