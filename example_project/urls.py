from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from views import stripe, view_payment, paybox

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/<payment_id>', view_payment, name='view_payment'),
    path('<payment_id>/paybox/authorize', paybox.authorize, name='paybox_authorize'),
    path('<payment_id>/paybox/capture', paybox.capture, name='paybox_capture'),
    # path('<payment_id>/paybox/refund', paybox.refund, name='aybox_refund'),
]

stripe_urls = [
    path('<payment_id>/stripe/checkout', stripe.checkout, name='stripe_checkout'),
    path('<payment_id>/stripe/elements_token', stripe.elements_token, name='stripe_elements_token'),

    path('<payment_id>/stripe/payment_intents_manual_flow', stripe.payment_intents_manual_flow,
         name='stripe_payment_intents_manual_flow'),
    path('<payment_id>/stripe/payment_intents_confirm_payment', stripe.payment_intents_confirm_payment,
         name='stripe_payment_intents_confirm_payment'),
    path('<payment_id>/stripe/capture', stripe.capture, name='stripe_capture'),
    path('<payment_id>/stripe/refund', stripe.refund, name='stripe_refund'),

    # path('<payment_id>/paybox/checkout', paybox.checkout, name='paybox_checkout'),
    # path('<payment_id>/paybox/process', paybox.process, name='paybox_process'),

]


urlpatterns += [path('stripe', include(stripe_urls))]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
