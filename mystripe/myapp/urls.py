from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns = [
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('create-checkout-session/<pk>/', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('', views.ProductLanding.as_view(), name='landing'),
    path('webhook/', views.stripe_webhook, name='webhook'),
    path('intent/<pk>', views.StripeIntent.as_view(), name='stripe-intent'),

]
