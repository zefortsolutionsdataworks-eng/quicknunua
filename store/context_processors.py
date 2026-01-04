from .models import Category
from .cart import Cart

def categories(request):
    """Make categories available to all templates"""
    return {
        'all_categories': Category.objects.filter(is_active=True, parent=None)
    }

def cart(request):
    """Make cart available to all templates"""
    return {'cart': Cart(request)}