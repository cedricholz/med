# import stripe
# from django.db.transaction import atomic
# from django.http import HttpResponseRedirect
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework.status import HTTP_204_NO_CONTENT
#
# from address.models import Address
# from api.MetaApi import MetaApi
# from api.sendgrid import SendgridApi
# from cart.models import CheckoutCart
# from cart_item.models import CartItem
# from line_item.models import LineItem
# from med.logger import Log
# from med.settings import STRIPE_SECRET_KEY
# from order.models import Order
# from product.models import Product
# from transaction.models import Transaction
# from util.util import get_first_and_last_name_from_full_name
#
# stripe.api_key = STRIPE_SECRET_KEY
#
#
# @csrf_exempt
# @api_view(['GET'])
# def cart_checkout_success(request):
#     session_id = request.query_params.get('session_id')
#     session = stripe.checkout.Session.retrieve(session_id)
#     try:
#
#         if session.payment_status == 'paid':
#             with atomic():
#                 customer_details = session.customer_details
#                 customer_address_data = customer_details.get('address')
#                 first_name, last_name = get_first_and_last_name_from_full_name(customer_details.get('name'))
#                 address = Address.objects.create(
#                     email=customer_details.get('email'),
#                     phone=customer_details.get('phone'),
#                     first_name=first_name,
#                     last_name=last_name,
#                     city=customer_address_data.get('city'),
#                     zip=customer_address_data.get('postal_code'),
#                     street1=customer_address_data.get('line1'),
#                     street2=customer_address_data.get('line2'),
#                     state=customer_address_data.get('state'),
#                     country=customer_address_data.get('country'),
#                 )
#                 order = Order.objects.create(
#                     address=address,
#                     type=Order.Type.APPAREL_AND_INVENTORY,
#                     status=Order.Status.PAID_AND_IN_PROGRESS
#                 )
#
#                 checkout_cart = CheckoutCart.objects.get(pk=session.metadata.get('checkout_cart_id'))
#                 for checkout_cart_item in checkout_cart.checkout_cart_items.all():
#                     cart_item = checkout_cart_item.cart_item
#                     if cart_item.quantity != checkout_cart_item.quantity:
#                         cart_item.quantity = checkout_cart_item.quantity
#
#                     cart_item.paid = True
#                     cart_item.save()
#
#                     line_item_price = 0
#                     product = cart_item.product
#                     product_variant = cart_item.product_variant
#
#                     if cart_item.type == CartItem.Type.APPAREL:
#                         line_item_price += product_variant.price
#                         product_variant.product.popularity += 1
#                         product_variant.product.save()
#                     elif cart_item.type == CartItem.Type.INVENTORY:
#                         product.status = Product.Status.SOLD
#                         cart_item.out_of_stock = True
#                         cart_item.save()
#                         product.save()
#                         line_item_price += product.price
#                         for option in product.options.all():
#                             line_item_price += option.price
#                     else:
#                         raise ValidationError("Invalid cart item type")
#
#                     line_item_total_price = line_item_price * cart_item.quantity
#
#                     LineItem.objects.create(
#                         order=order,
#                         product=cart_item.product,
#                         product_variant=cart_item.product_variant,
#                         quantity=cart_item.quantity,
#                         price=line_item_price,
#                         total_price=line_item_total_price,
#                         type=cart_item.type,
#                     )
#
#                 total_details = session.total_details
#                 Transaction.objects.get_or_create(
#                     order=order,
#                     session_id=session_id,
#                     payment_intent_id=session.payment_intent,
#                     type=Transaction.Type.STRIPE,
#                     amount_subtotal=session.amount_subtotal / 100,
#                     amount_total=session.amount_total / 100,
#                     amount_tax=total_details.amount_tax / 100,
#                 )
#
#                 order.update_payments_and_costs()
#
#                 SendgridApi().send_cart_checkout_success_email(order)
#
#             order.send_to_dreamship()
#             response = HttpResponseRedirect(f"/checkout-success")
#             response = MetaApi().set_purchase_data_cookie(order, response)
#             return response
#
#     except Exception as exc:
#         payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
#         charge_id = payment_intent.latest_charge
#         refund_id = None
#         if charge_id:
#             refund = None
#             refund_id = ""
#             try:
#                 refund = stripe.Refund.create(
#                     charge=charge_id,
#                 )
#             except Exception:
#                 pass
#
#             if refund:
#                 refund_id = refund.id
#
#             SendgridApi().send_checkout_failed_email(order, refund_id, exc)
#
#         Log.error(
#             "cart_checkout_success FAILED", exc=exc, data={
#                 'session_id': session_id,
#                 'charge_id': charge_id,
#                 'refund_id': refund_id,
#             }
#         )
#         return HttpResponseRedirect("/checkout-failed")
#
#
# @csrf_exempt
# @api_view(['GET'])
# def cart_checkout_cancel(request):
#     return Response(status=HTTP_204_NO_CONTENT)
#
#
# @csrf_exempt
# @api_view(['GET'])
# def custom_order_checkout_success(request):
#     session_id = request.query_params.get('session_id')
#
#     session = stripe.checkout.Session.retrieve(session_id)
#     order = None
#     try:
#         order = Order.objects.get(pk=session.metadata.get('order_id'), type=Order.Type.CUSTOM)
#         is_deposit = session.metadata.get('is_deposit') == 'True'
#         transaction, created = Transaction.objects.get_or_create(
#             session_id=session_id,
#             payment_intent_id=session.payment_intent,
#             type=Transaction.Type.STRIPE,
#             order=order,
#             is_deposit=is_deposit
#         )
#
#         if session.payment_status == 'paid':
#             with atomic():
#                 customer_details = session.customer_details
#                 customer_address_data = customer_details.get('address')
#
#                 address = order.address
#                 address.city = customer_address_data.get('city')
#                 address.zip = customer_address_data.get('zip')
#                 address.street1 = customer_address_data.get('street1')
#                 address.street2 = customer_address_data.get('street2')
#                 address.state = customer_address_data.get('state')
#                 address.country = customer_address_data.get('country')
#                 address.save()
#
#                 total_details = session.total_details
#                 transaction.amount_subtotal = session.amount_subtotal / 100
#                 transaction.amount_total = session.amount_total / 100
#                 transaction.amount_tax = total_details.amount_tax / 100
#                 transaction.save()
#                 order.locked = True
#                 order.update_payments_and_costs()
#
#                 if is_deposit:
#                     SendgridApi().send_deposit_received_email(
#                         order=order,
#                         amount_subtotal=transaction.amount_subtotal,
#                         amount_total=transaction.amount_total,
#                         amount_tax=transaction.amount_tax,
#                     )
#                 else:
#                     SendgridApi().send_balance_paid_email(
#                         order=order,
#                         amount_subtotal=transaction.amount_subtotal,
#                         amount_total=transaction.amount_total,
#                         amount_tax=transaction.amount_tax,
#                     )
#
#             response = HttpResponseRedirect(f"/custom-surfboard-order/{order.customer_facing_id}/")
#             response = MetaApi().set_purchase_data_cookie(order, response)
#             return response
#
#     except Exception as exc:
#         payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
#         charge_id = payment_intent.latest_charge
#         refund_id = None
#         if charge_id:
#             refund = None
#             refund_id = ""
#             try:
#                 refund = stripe.Refund.create(
#                     charge=charge_id,
#                 )
#             except Exception:
#                 pass
#
#             if refund:
#                 refund_id = refund.id
#             SendgridApi().send_checkout_failed_email(order, refund_id, exc)
#
#         Log.error(
#             "custom_order_checkout_success FAILED", exc=exc, data={
#                 'session_id': session_id,
#                 'charge_id': charge_id,
#                 'refund_id': refund_id,
#             }
#         )
#         return HttpResponseRedirect("/checkout-failed")
