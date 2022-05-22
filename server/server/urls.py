from django.contrib import admin
from django.urls import path

from stripe_app.views import (
    main_page, item_info, create_checkout_session, success_page, cancel_page,
    add_to_order, show_bucket, create_checkout_session_to_order, clear_bucket
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name="main"),
    path('item/<int:pk>', item_info, name="item"),
    path('buy/<int:pk>', create_checkout_session, name="buy"),
    path('to-order', add_to_order, name='add-to-order'),
    path('bucket', show_bucket, name="bucket"),
    path('buy-bucket', create_checkout_session_to_order, name="buy-bucket"),
    path('success', success_page, name="success"),
    path('cancel', cancel_page, name="cancel"),
    path('clear', clear_bucket, name="clear")
]
