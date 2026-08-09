from .models import Category

def cart_context(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0
    categories = Category.objects.all()
    return {
        'cart_count': cart_count,
        'global_categories': categories,
    }
