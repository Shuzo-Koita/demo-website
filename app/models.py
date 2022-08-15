from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=255, 
        unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=False)
    
    updated = models.DateTimeField(
        auto_now=True,
        editable=False)
        
    title = models.CharField(
        max_length=255)
        
    body = models.TextField(
        blank=True)
        
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE)
        
    tags = models.ManyToManyField(
        Tag,
        blank=True)
    
    image = models.ImageField(
        upload_to='post',
        null=True,
        blank=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False)
    
    updated = models.DateTimeField(
        auto_now=True,
        editable=False)

    name = models.CharField(
        max_length=255,
        unique=True)

    # slug = models.SlugField(
    #     max_length=255, 
    #     unique=True)

    description = models.TextField(
        blank=True)

    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE)
        
    price = models.IntegerField()

    image = models.ImageField(
        upload_to='product', 
        blank=True)

    stock = models.IntegerField()

    available = models.BooleanField(
        default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
 
    def __str__(self):
        return '{}'.format(self.name)

class LikeForProduct(models.Model):
    """投稿に対するいいね"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, blank=True)
    furigana = models.CharField(max_length=255, blank=True)
    postal = models.CharField(max_length=255, blank=True)
    pref_id = models.CharField(max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    email2 = models.EmailField(blank=True)
    tel = models.CharField(max_length=255, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.email