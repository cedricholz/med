import base64
import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from api.sendgrid import SendgridApi
from line_item.models import LineItem
from med.logger import Log
from order.models import Order
from tracking.models import Tracking


@csrf_exempt
@api_view(["POST"])
def dreamship_webhook(request):
    try:

        webhook_data = json.loads(request.body)
        if webhook_data.get('event', {}).get('action') == 'order-status-updated':
            data = webhook_data.get('data')
            try:
                order = Order.objects.get(external_id=data.get('id'))
            except Exception:
                order = Order.objects.get(pk=data.get('reference_id'))
            order.dreamship_status = data.get('status')
            order.save()
            for fulfillments_data in data.get('fulfillments'):
                line_items = LineItem.objects.filter(
                    pk__in=[line_item_data.get('reference_id') for line_item_data in
                            fulfillments_data.get('line_items')]
                )
                if len(fulfillments_data.get('trackings')) > 0:
                    tracking_data = fulfillments_data.get('trackings')[0]
                    tracking_number = tracking_data.get('tracking_number')
                    carrier = tracking_data.get('carrier')
                    tracking_url = tracking_data.get('tracking_url')
                    tracking, created = Tracking.objects.get_or_create(
                        order=order,
                        tracking_number=tracking_number,
                        carrier=carrier,
                        defaults={
                            "tracking_url": tracking_url,
                        }
                    )
                    if created:
                        for line_item in line_items:
                            line_item.tracking = tracking
                            line_item.complete = True
                            line_item.save()
                        SendgridApi().send_tracking_email(tracking)
            if data.get('status') == 'shipped':
                if not order.line_items.filter(product__isnull=False).exists():
                    order.status = Order.Status.COMPLETE
                    order.save()
        return Response(status=HTTP_204_NO_CONTENT)
    except Exception as exc:
        Log.error(title="dreamship_webhook", exc=exc)
        return Response(status=HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(["POST"])
def gmail_webhook(request):
    if request.method == 'POST':
        try:
            webhook_data = json.loads(request.body)
            data = webhook_data.get('message', {}).get('data')
            message = base64.urlsafe_b64decode(data).decode('utf-8')
            print(message)
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as exc:
            return Response(status=HTTP_204_NO_CONTENT)