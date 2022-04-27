from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('payment', views.PaymentAPI, basename='payment')

urlpatterns = [

    path('a/', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('create-checkout-session/<pk>/', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('', views.ProductLanding.as_view(), name='landing'),
    path('webhook/', views.stripe_webhook, name='webhook'),
    path('intent/<pk>', views.StripeIntent.as_view(), name='stripe-intent'),
    path('create/', views.ProductCreate.as_view(), name='create'),
    path('list/', views.ProductList.as_view(), name='home'),
    path('detail/<id>/', views.ProductDetail.as_view(), name='detail'),
    path('history/', views.OrderHistory.as_view(), name='history'),
    path('failed/', views.PaymentFailed.as_view(), name='failed'),


]
