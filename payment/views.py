from django.shortcuts import render
from arts.models import Art
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
# Create your views here.
def checkOut(request, art_id):

    art = Art.objects.get(id=art_id)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': art.price,
        'item_name': art.title,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs = {'art_id': art.id})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'art_id': art.id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'art': art,
        'paypal': paypal_payment
    }

    return render(request, 'payments/checkout.html', context)

def paymentSuccessful(request, art_id):

    art = Art.objects.get(id=art_id)

    return render(request, 'payments/payment-success.html', {'art': art})

def paymentFailed(request, art_id):

    art = Art.objects.get(id=art_id)

    return render(request, 'payments/payment-failed.html', {'art': art})
