from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=False)
    slug = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to="photos/categories", blank=True)

    class Meta: # how will be shown in Django admin panel
        verbose_name= "category" # when singular
        verbose_name_plural = "categories" # when plural

    def get_url(self):
        return reverse("products_by_category", args=[self.slug])

    def __str__(self) -> str:
        return self.category_name + ": " + self.slug