from django.db import models

from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # on_delete = cuando elimine el producto relacionado, que también se elimine el cart item, el record
    variations = models.ManyToManyField(Variation, blank=True) # manytomanyfield = saves a data collection
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # on_delete = cuando elimine el producto relacionado, que también se elimine el cart item, el record
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True) 

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self) -> str:
        return self.product