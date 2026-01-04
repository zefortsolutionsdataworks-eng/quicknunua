from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('track-order/', views.track_order, name='track_order'),
    path('help/', views.help_center, name='help_center'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('returns/', views.returns, name='returns'),
    path('careers/', views.careers, name='careers'),
]