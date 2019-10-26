from django.contrib import admin
from django.urls import path, include
import views
from views import stripe, view_payment, paybox, netaxept

example_urlpatterns = [
    path('', views.list_payments, name='list_payments'),
    path('<payment_id>', views.view_payment, name='view_payment'),
    path('<payment_id>/paybox/authorize', paybox.authorize, name='paybox_authorize'),
    path('<payment_id>/paybox/capture', paybox.capture, name='paybox_capture'),
    path('stripe/', include(stripe.urls)),
    path('netaxept/', include(netaxept.urls)),
    path('paybox/', include(paybox.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls')),
    path('example/', include(example_urlpatterns)),
]
