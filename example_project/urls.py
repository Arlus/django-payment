from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import views
from views import netaxept
from views import stripe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/<payment_id>', views.view_payment, name='view_payment'),
    path('capture/<payment_id>', views.capture, name='capture'),
    path('refund/<payment_id>', views.refund, name='refund'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

stripe_urls = [
    path('elements_token/<payment_id>', stripe.elements_token, name='stripe_elements_token'),
    path('checkout/<payment_id>', stripe.checkout, name='stripe_checkout'),
    path('payment_intents_manual_flow/<payment_id>', stripe.payment_intents_manual_flow,
         name='stripe_payment_intents_manual_flow'),
    path('payment_intents_confirm_payment/<payment_id>', stripe.payment_intents_confirm_payment,
         name='stripe_payment_intents_confirm_payment'),
]

netaxept_urls = [
    path('authorize/<payment_id>', netaxept.authorize, name='netaxept_authorize'),
]

urlpatterns += [
    path('stripe/', include(stripe_urls)),
    path('netaxept/', include(netaxept_urls)),
]
