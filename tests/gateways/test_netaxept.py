from django.test import TestCase
from netaxept import actions
from netaxept.actions import PaymentRegistrationNotCompleted
from netaxept.models import Payment
from pytest import raises, mark


class PaymentTest(TestCase):

    @mark.skip('because it tries to invoke the real netaxept gateway')
    def test_a_successful_payment_can_go_on_thru_sale(self):
        payment = Payment.objects.create(
            transaction_id='1234567890',
            order_number='an-order-number',
            amount=100,
            currency_code='NOK',
            success=True,
            auto_auth=False)
        actions.sale(payment.id)

    def test_an_unsuccesful_payment_cannot_go_on_thru_sale(self):
        payment = Payment.objects.create(
            transaction_id='1234567890',
            order_number='an-order-number',
            amount=100,
            currency_code='NOK',
            success=False,
            auto_auth=False)
        with raises(PaymentRegistrationNotCompleted):
            actions.sale(payment.id)
