# Netaxept

## Configuration

In the PAYMENT_GATEWAYS setting, configure the netaxept connection params:

`merchant_id`, `token`, `wsdl`, and `terminal`.

The production wsdl and terminal are:

`https://epayment.nets.eu/netaxept.svc?wsdl`

`https://epayment.nets.eu/Terminal/default.aspx`


## Notes

Amounts are in smallest currenty unit. For instance one NOK is represented inside netaxept as "100 NOK"


## Netaxept Reference

https://shop.nets.eu/web/partners/home

Read this first: https://shop.nets.eu/web/partners/flow-outline

API details: https://shop.nets.eu/web/partners/appi

Test card numbers: https://shop.nets.eu/web/partners/test-cards
