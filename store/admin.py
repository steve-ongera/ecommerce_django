from django.contrib import admin
from .models import Product, Variation

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {"slug": ("product_name", )} # auto fill slug with product name
    list_display= ("product_name", "price", "stock", "category", "is_available","modified_date")

class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", 'variation_value', "is_active")
    list_editable = ("is_active", ) # this line makes 'is_active' checkbox, editable in the table of admin dashboard
    list_filter = ("product", "variation_category", "variation_value", "is_active") # this line adds a column to filter in admin dashboard

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)