from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product, Profile
from django.http import JsonResponse
from django.contrib import messages
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = len(cart)

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Produit ajouté au panier...")
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, "Article supprimé du panier...")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Votre panier a été mis à jour...")
        return response

def order_success(request):
    return render(request, 'order_success.html')

def checkout_view(request):
    shipping_form = ShippingForm()
    cart = Cart(request)

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()

            order = Order.objects.create(
                user=request.user,
                full_name=shipping_address.shipping_full_name,
                email=shipping_address.shipping_email,
                shipping_address=str(shipping_address),
                amount_paid=cart.cart_total(),
                status='pending'
            )

            for product in cart.get_prods():
                order_qty = cart.get_quants()[str(product.id)]
                
                # Decrease product quantity
                product.quantity -= order_qty
                product.save()
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    user=request.user,
                    quantity=order_qty,
                    price=product.price
                )

            cart.clear_cart()
            messages.success(request, 'Commande passée avec succès !')
            return redirect('order_success')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire expédition.')

    context = {
        'shipping_form': shipping_form,
        'cart_products': cart.get_prods(),
        'quantities': cart.get_quants(),
        'totals': cart.cart_total()
    }

    return render(request, 'checkout.html', context)