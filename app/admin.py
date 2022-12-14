from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(models.LikeForProduct)
class LikeAdmin(admin.ModelAdmin):
    pass