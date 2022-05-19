from django.contrib import admin
from django.urls import path

from stripe_app.views import (
    main_page, item_info, create_checkout_session, success_page, cancel_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name="main"),
    path('item/<int:pk>', item_info, name="item"),
    path('buy/<int:pk>', create_checkout_session, name="buy"),
    path('success', success_page, name="success"),
    path('cancel', cancel_page, name="cancel")
]
