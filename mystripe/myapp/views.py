import json
from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import Product
from django.http import JsonResponse, HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class ProductLanding(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name='Samsung')
        context = super(ProductLanding, self).get_context_data(**kwargs)
        context.update({
            'product': product,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)

        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {'currency': 'inr',
                                   'unit_amount': product.price,
                                   'product_data': {'name': product.name}},
                    # 'price': product.price,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({
            'pk': checkout_session.url
        })


# endpoint_secret = 'whsec_RkOURLr7uAcQfQZrV72AjdMoEm6o2AYp'


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        print(product_id)
        product = Product.objects.get(id=product_id)
        print(product)
        send_mail(
            subject="Here Is Your Product",
            message=f"ThankYou for Buy a Product. the url is {product.url}",
            recipient_list=[customer_email],
            from_email="raj.kanani@plutustec.com"
        )

        # Fulfill the purchase...
        print(session)
    # Passed signature verification
    return HttpResponse(status=200)


class StripeIntent(View):
    def post(self, request, *args, **kwargs):

        try:
            product = Product.objects.get(id=self.kwargs["pk"])
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='inr',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
