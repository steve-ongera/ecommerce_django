from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist

from .models import Cart, CartItem
from store.models import Product, Variation

# Create your views here.

# private function = _before_function
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            # check if the varation exist in the db
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass



    try:
        # cart_id= actual session of user in browser
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    isCartItemExist= CartItem.objects.filter(product=product, cart=cart).exists()
    if isCartItemExist: 
        # cartitem is the info of the product that user will buy
        cart_item = CartItem.objects.filter(product=product, quantity=1, cart=cart)

        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else: # create cart 
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )

        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
        
    return redirect("cart")

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)# consulta en función del producto y del carrito
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save() # save the change in db
    else:
        cart_item.delete()
    
    return redirect("cart")

def delete_all_items_in_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart")

def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0

    try: 
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items: # know final price of all the cart
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100 # tax of 2%
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass

    # what will send to the html template
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, "store/cart.html", context)