import os
import stripe

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from stripe_app.models import Item

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def main_page(request):
    items = Item.objects.all()
    return render(request, 'main.html', context={"items": items})


def item_info(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        return HttpResponse(f"<h1>Item with id={pk} not found</h1>")
    return render(request, 'item_info.html', context={"item": item, "STRIPE_PUBLIC": os.getenv("STRIPE_PUBLIC_KEY")})


def create_checkout_session(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        return HttpResponse(f"<h1>Item with id={pk} not found</h1>")

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )

    return JsonResponse({
        'id': session.id
    })


def success_page(request):
    return render(request, 'success.html')


def cancel_page(request):
    return render(request, 'cancel.html')
