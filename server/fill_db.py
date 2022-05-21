from uuid import uuid4
from stripe_app.models import Item, Discount, PromoCode

from django.db.utils import IntegrityError

Item.objects.bulk_create([
    Item(name='iPhone X', description='Хороший смартфон', price=55000),
    Item(name='iPhone 11', description='Отличный смартфон', price=65000),
    Item(name='iPhone 12', description='Великолепный смартфон', price=80000),
    Item(name='MacBook Pro 13 M1', description='Один из лучших в мире', price=180000)
])

uuid_d1 = uuid4()
uuid_d2 = uuid4()
uuid_d3 = uuid4()

Discount.objects.bulk_create([
    Discount(uuid=uuid_d1, percent_off=25, duration='once'),
    Discount(uuid=uuid_d2, percent_off=15, duration='repeating', duration_in_months=3),
    Discount(uuid=uuid_d3, percent_off=10, duration='forever')
])

try:
    PromoCode.objects.bulk_create([
        PromoCode(coupon=Discount.objects.get(uuid=uuid_d1), code='STRIPE25'),
        PromoCode(coupon=Discount.objects.get(uuid=uuid_d2), code='RANKS15'),
        PromoCode(coupon=Discount.objects.get(uuid=uuid_d2), code='STRIPE15'),
        PromoCode(coupon=Discount.objects.get(uuid=uuid_d2), code='APP15'),
        PromoCode(coupon=Discount.objects.get(uuid=uuid_d1), code='RANKS')
    ])
except IntegrityError:
    pass
