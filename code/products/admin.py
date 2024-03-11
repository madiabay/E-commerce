from django.contrib import admin
from . import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImages
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_top', 'is_active',
    list_editable = 'is_top', 'is_active',
    search_fields = 'title', 'body',
    inlines = ProductImageInline,


admin.site.register(models.ProductImages)
admin.site.register(models.Product, ProductAdmin)
