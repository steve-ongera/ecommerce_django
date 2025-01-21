from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)} # auto fill slug with category_name. Replacing " " with "-"
    list_display = ("category_name", "slug")

# Register your models here.
admin.site.register(Category, CategoryAdmin)