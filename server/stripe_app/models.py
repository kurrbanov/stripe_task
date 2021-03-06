from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)

    def get_display_price(self):
        return f"{(self.price / 100):.2f}"

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]


class Order(models.Model):
    uuid = models.UUIDField(unique=True)
    discount = models.ManyToManyField('Discount', blank=True)
    jurisdiction = models.CharField(max_length=2, default='RU')

    def __str__(self):
        return str(self.uuid)

    class Meta:
        indexes = [
            models.Index(fields=['uuid'])
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.order} - {self.item}"


class Discount(models.Model):
    DURATION = (
        ('forever', 'forever'),
        ('once', 'once'),
        ('repeating', 'repeating')
    )
    uuid = models.UUIDField(unique=True)
    percent_off = models.IntegerField()
    duration = models.CharField(choices=DURATION, max_length=9)
    duration_in_months = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f"{self.percent_off}%"

    class Meta:
        indexes = [
            models.Index(fields=['uuid'])
        ]


class PromoCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    coupon = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}"

    class Meta:
        indexes = [
            models.Index(fields=['code'])
        ]


class Tax(models.Model):
    JURISDICTION = (
        ('US', 'US'),
        ('DE', 'DE'),
        ('RU', 'RU')
    )

    DISPLAY_NAME = (
        ('sales_tax', 'sales_tax'),
        ('vat', 'vat')
    )

    tax_id = models.CharField(max_length=255)
    display_name = models.CharField(choices=DISPLAY_NAME, max_length=10)
    jurisdiction = models.CharField(choices=JURISDICTION, max_length=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    inclusive = models.BooleanField()

    def __str__(self):
        return f"{self.jurisdiction} - {self.percentage}%"

    class Meta:
        indexes = [
            models.Index(fields=['jurisdiction', 'tax_id'])
        ]
