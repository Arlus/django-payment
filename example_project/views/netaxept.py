"""
Example views for interactive testing of payment with netaxept.

You should restrict access (maybe with 'staff_member_required') if you choose to add this to your urlconf.
"""

from django.forms import forms, IntegerField, BooleanField, CharField, URLField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def authorize(request: HttpRequest, payment_id: int) -> HttpResponse:
    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            registration = register(
                order_number=form.cleaned_data['order_number'],
                amount=form.cleaned_data['amount'],
                currency_code=form.cleaned_data['currency_code'],
                redirect_url=form.cleaned_data['redirect_url'],
                auto_auth=form.cleaned_data['auto_auth'],
            )
            return redirect(get_payment_terminal_url(registration.transaction_id))
    else:
        form = PayForm()

    return render(request, 'netaxept/example/form.html', {
        'title': 'Payment',
        'form': form
    })
