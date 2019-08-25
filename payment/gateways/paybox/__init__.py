from typing import Dict

from . import connect
from .utils import (
    get_amount_for_paybox,
    get_amount_from_paybox,
    get_currency_for_paybox,
    get_currency_from_paybox,
    verify_amount,
    verify_cle,
    verify_identifiant,
    verify_rang,
    verify_site
)
from ...interface import GatewayConfig, GatewayResponse, PaymentData
from .paybox_system import PayboxSystemClient


def get_client_token(**_):
    """Not implemented for Paybox gateway currently.
    """
    return


def authorize(
        payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    client, error = _get_client(**config.connection_params), None

    client.post_to_paybox(operation_type="Authorization", amount=get_amount_for_paybox(payment_information.amount),
                          currency=get_currency_for_paybox(payment_information.currency), cmd=payment_information.order_id,
                          email=payment_information.customer_email)
    form = client.construct_form()

    return form


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    client, error = _get_client(**config.connection_params), None
    client.post_to_paybox(operation_type="Capture", amount=get_amount_for_paybox(payment_information.amount),
                          currency=get_currency_for_paybox(payment_information.currency), cmd=payment_information.order_id,
                          email=payment_information.customer_email)
    form = client.construct_form()
    return form


# def refund(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
#     client, error = _get_client(**config.connection_params), None
#
#     client.post_to_paybox(operation_type="Refund", amount=get_amount_for_paybox(payment_information.amount),
#                           currency=get_currency_for_paybox(payment_information.currency))
#     form = client.construct_html_form()
#     return form


def _get_client(**connection_params):
    paybox_system_client = PayboxSystemClient(**connection_params)
    return paybox_system_client


def _get_paybox_charge_payload(
        payment_information: PaymentData, should_capture: bool
) -> Dict:
    # Get currency
    currency = get_currency_for_paybox(payment_information.currency)

    # Get appropriate amount for stripe
    paybox_amount = get_amount_for_paybox(payment_information.amount)

    # Construct the charge payload from the data
    charge_payload = {
        "capture": should_capture,
        "amount": paybox_amount,
        "currency": currency,
        "source": payment_information.token,
        # "description": name,
        "metadata": payment_information.metadata,
    }

    return charge_payload


def _create_response(
        payment_information: PaymentData, kind: str, response: Dict, error: str
) -> GatewayResponse:
    # Get currency from response or payment
    currency = get_currency_from_paybox(
        response.get("currency")
    )

    amount = payment_information.amount
    # Get amount from response or payment
    if "amount" in response:
        paybox_amount = response.get("amount")
        if "amount_refunded" in response:
            # This happens for partial catpure which will refund the left
            # Then the actual amount should minus refunded amount
            paybox_amount -= response.get("amount_refunded")  # type:ignore
        amount = get_amount_from_paybox(paybox_amount)

    # Get token from response or use provided one
    token = response.get("id", payment_information.token)

    # Check if the response's status is flagged as succeeded
    is_success = response.get("status") == "succeeded"
    return GatewayResponse(
        is_success=is_success,
        transaction_id=token,
        kind=kind,
        amount=amount,
        currency=currency,
        error=error,
        raw_response=response,
    )

