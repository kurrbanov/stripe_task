from django.shortcuts import render
from django.http import HttpResponse

from stripe_app.models import Item


def main_page(request):
    items = Item.objects.all()
    return render(request, 'main.html', context={"items": items})


def item_info(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        return HttpResponse(f"<h1>Item #{pk} not found</h1>")
    return render(request, 'item_info.html', context={"item": item})
