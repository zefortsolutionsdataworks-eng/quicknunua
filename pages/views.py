from django.shortcuts import render

def about(request):
    """About Us page"""
    return render(request, 'pages/about.html')

def contact(request):
    """Contact Us page"""
    return render(request, 'pages/contact.html')

def track_order(request):
    """Track Order page"""
    return render(request, 'pages/track_order.html')

def help_center(request):
    """Help Center page"""
    return render(request, 'pages/help_center.html')

def terms(request):
    """Terms & Conditions page"""
    return render(request, 'pages/terms.html')

def privacy(request):
    """Privacy Policy page"""
    return render(request, 'pages/privacy.html')

def returns(request):
    """Returns & Refunds page"""
    return render(request, 'pages/returns.html')

def careers(request):
    """Careers page"""
    return render(request, 'pages/careers.html')