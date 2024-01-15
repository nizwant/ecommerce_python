from django.shortcuts import render, redirect
from .models import CartItem, Order, OrderItem
from django.contrib import messages
from .forms import OrderForm
from product_page.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, "cart_and_orders/cart.html", {"cart_items": cart_items})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart")


@csrf_exempt
@require_POST
def update_quantity(request):
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity")
    cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
    cart_item.quantity = quantity
    cart_item.save()
    return JsonResponse({"status": "ok"})


@csrf_exempt
@require_POST
def remove_item(request):
    product_id = request.POST.get("product_id")
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({"status": "ok"})


def finalize_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    form = OrderForm(user=request.user)
    return render(
        request,
        "cart_and_orders/finalize_order.html",
        {"cart_items": cart_items, "total_price": total_price, "form": form},
    )


def place_order(request):
    # # Get the user's cart items
    # cart_items = CartItem.objects.filter(user=request.user)

    # # Create a new order and add the cart items to it
    # order = Order.objects.create(user=request.user)
    # for item in cart_items:
    #     order.items.add(item.product)

    # # Clear the user's cart
    # cart_items.delete()

    # # Add a flash message
    # messages.success(request, "Your order was saved correctly.")

    # # Redirect to the product index page
    return redirect("product_index")
