import os
import uuid
import stripe

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.db import transaction, IntegrityError, DatabaseError

from stripe_app.models import Item, Order, OrderItem, Discount, PromoCode, Tax

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def main_page(request):
    items = Item.objects.all()
    return render(request, 'main.html', context={"items": items})


def success_page(request):
    return render(request, 'success.html')


def cancel_page(request):
    return render(request, 'cancel.html')


def item_info(request, pk):
    res = 1 / 0
    item = Item.objects.filter(id=pk).first()
    if item is None:
        return HttpResponse(f"<h1>Item with id={pk} not found</h1>")

    context = {
        "item": item,
        "STRIPE_PUBLIC": os.getenv("STRIPE_PUBLIC_KEY")
    }
    if "order_id" not in request.session:
        context["order_cnt"] = 0
    else:
        order = Order.objects.get(uuid=uuid.UUID(request.session.get("order_id")))
        orders_to_cnt = 0
        for o_i in OrderItem.objects.filter(order=order):
            orders_to_cnt += o_i.quantity
        context["order_cnt"] = orders_to_cnt

    return render(request, 'item_info.html', context=context)


def create_checkout_session(request, pk):
    item = Item.objects.filter(id=pk).first()
    if item is None:
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


def add_to_order(request):
    if request.method == "POST":
        try:
            if "order_id" not in request.session:
                request.session.set_expiry(60 * 60 * 24)
                order_uuid = uuid.uuid4()
                request.session["order_id"] = str(order_uuid)
                order = Order(uuid=order_uuid)
                item = Item.objects.get(id=request.POST.get("item_id"))
                order_item = OrderItem(order=order, item=item)
                with transaction.atomic():
                    order.save()
                    order_item.save()
            else:
                item = Item.objects.get(id=request.POST.get("item_id"))
                order = Order.objects.get(uuid=uuid.UUID(request.session.get("order_id")))
                try:
                    order_item = OrderItem.objects.get(order=order, item=item)
                    with transaction.atomic():
                        order_item.quantity += 1
                        order_item.save()
                except OrderItem.DoesNotExist:
                    with transaction.atomic():
                        order_item = OrderItem(order=order, item=item)
                        order_item.save()
            orders_to_cnt = 0
            for o_i in OrderItem.objects.filter(order=order):
                orders_to_cnt += o_i.quantity
            context = {
                "item": item,
                "STRIPE_PUBLIC": os.getenv("STRIPE_PUBLIC_KEY"),
                "order_cnt": orders_to_cnt
            }
            return render(request, 'item_info.html', context=context)
        except Item.DoesNotExist:
            return HttpResponse("NOT FOUND")
    return HttpResponse("NOT ALLOWED")


def show_bucket(request):
    order = Order.objects.filter(uuid=uuid.UUID(request.session.get("order_id"))).order_by("id").first()
    order_item = OrderItem.objects.filter(order=order)

    if order is None or order_item is None:
        return render(request, 'orders.html', context={"empty": True})

    context = {
        "empty": False,
        "countries": Tax.JURISDICTION,
        "order_item": order_item,
        "STRIPE_PUBLIC": os.getenv("STRIPE_PUBLIC_KEY"),
        "order": order
    }

    if request.method == "POST":
        with transaction.atomic():
            order.jurisdiction = request.POST.get("country")
            order.save()
    return render(request, 'orders.html', context=context)


@transaction.atomic
def create_checkout_session_to_order(request):
    order = Order.objects.filter(uuid=uuid.UUID(request.session.get("order_id"))).order_by("id").first()
    if order is None:
        return HttpResponse("NOT FOUND")

    order_item = OrderItem.objects.filter(order=order)

    coupons_id_list = [coupon.id for coupon in stripe.Coupon.list()]
    for discount in Discount.objects.all():
        if discount.duration == "forever" or discount.duration == "once":
            with transaction.atomic():
                discount.duration_in_months = None
                discount.save()
        if str(discount.uuid) not in coupons_id_list:
            stripe.Coupon.create(
                id=str(discount.uuid),
                percent_off=discount.percent_off,
                duration=discount.duration,
                duration_in_months=discount.duration_in_months
            )
            with transaction.atomic():
                order.discount.add(discount)
                order.save()

    promo_codes = [{promo.code: promo.id} for promo in stripe.PromotionCode.list()]
    for promo in PromoCode.objects.all():
        check_list = list(filter(lambda x: True if promo.code in x else False, promo_codes))
        if not check_list:
            stripe.PromotionCode.create(
                coupon=str(promo.coupon.uuid),
                code=promo.code
            )
        else:
            stripe.PromotionCode.modify(check_list[0].get(promo.code), metadata={"coupon": promo.coupon.uuid})

    for tax in Tax.objects.all():
        new_tax = stripe.TaxRate.create(
            display_name=tax.display_name,
            jurisdiction=tax.jurisdiction,
            percentage=tax.percentage,
            inclusive=tax.inclusive
        )
        with transaction.atomic():
            tax.tax_id = new_tax.id
            tax.save()

    items = []

    tax_order = Tax.objects.filter(jurisdiction=order.jurisdiction).order_by("id").first()
    if tax_order is None:
        return HttpResponse("NOT FOUND")

    for item in order_item:
        with transaction.atomic():
            item.tax = tax_order
            item.save()

        items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.item.name,
                },
                'unit_amount': item.item.price,
            },
            'quantity': item.quantity,
            'tax_rates': [item.tax.tax_id]
        })

    session = stripe.checkout.Session.create(
        line_items=items,
        mode='payment',
        allow_promotion_codes=True,
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )

    return JsonResponse({
        'id': session.id
    })
