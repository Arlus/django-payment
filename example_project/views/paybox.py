from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from structlog import get_logger

# from payment import get_payment_gateway
from payment.models import Payment
from payment.utils import paybox_gateway_authorize, paybox_gateway_capture

logger = get_logger()


def authorize(request: HttpRequest, payment_id: int) -> HttpResponse:
    payment = get_object_or_404(Payment, id=payment_id)
    form = paybox_gateway_authorize(payment=payment)
    return TemplateResponse(request, 'paybox/operation.html', {'form': form})


def capture(request: HttpRequest, payment_id: int) -> HttpResponse:
    payment = get_object_or_404(Payment, id=payment_id)
    form = paybox_gateway_capture(payment=payment)
    return TemplateResponse(request, 'paybox/operation.html', {'form': form})


# def process(request: HttpRequest, payment_id: int) -> HttpResponse:
#     payment = get_object_or_404(Payment, id=payment_id)
#     capture_result = gateway_process_payment(payment=payment)
#     logger.info('paybox process', payment=payment, capture_result=capture_result)
#     return redirect('view_payment', payment_id=payment_id)
#
#
# def refund(request: HttpRequest, payment_id: int) -> HttpResponse:
#     payment = get_object_or_404(Payment, id=payment_id)
#     refund_result = gateway_refund(payment=payment)
#     logger.info('paybox refund', payment=payment, refund_result=refund_result)
#     return redirect('view_payment', payment_id=payment_id)
#
#
# def checkout(request: HttpRequest, payment_id: int) -> HttpResponse:
#     """
#     Takes the user to the Paybox checkout page.
#     This is not part of the gateway abstraction, so we implement it directly using the Paybox System pages
#     """
#     payment = get_object_or_404(Payment, id=payment_id)
#     payment_gateway, gateway_config = get_payment_gateway(payment.gateway)
#     connection_params = gateway_config.connection_params
#     form = payment_gateway.create_form(payment_information=payment, gateway_params=connection_params)
#     endpoint = get_paybox_system_endpoint_url(production=gateway_config.connection_paramsget('production'))
#     return TemplateResponse(request, 'paybox/checkout.html', {'form': form, 'action': endpoint, 'method': "POST"})
