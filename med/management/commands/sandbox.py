import stripe
from django.core.management.base import BaseCommand

from api.sendgrid import SendgridApi
from med.settings import STRIPE_SECRET_KEY
from option.models import Option
from order.models import Order
from site_configuration.models import SiteConfiguration
from util.aws import get_presigned_put_url

stripe.api_key = STRIPE_SECRET_KEY


class Command(BaseCommand):
    def handle(self, *args, **kwargs):


        return
        for order in Order.objects.all():
            print(order.id)
            order.update_payments_and_costs()

        return
        api = SendgridApi()
        data = {
            "name": "ced",
            "email": "cedricholz@gmail.com",
            "phone": "1234123123",
            "message": "wooooroorkrkk",
        }
        files = data.get('files', [])
        try:
            api.send_contact_email(
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
                message_text=data.get("message"),
                files=files,
                raise_error=True
            )
        except Exception as exc:
            print(str(exc.body))
            print()

        return
        url = get_presigned_put_url()
        print(url)

        return
        order = Order.objects.get(customer_facing_id="S5B2VDPVGJ")
        print(order.comment.text)

        return
        "#7e8182"
        site_configuration, created = SiteConfiguration.objects.get_or_create()
        Option.objects.filter(
            value="#7e8182",
        ).delete()

        Option.objects.create(
            site_configuration=site_configuration,
            type=Option.Type.BOTTOM_COLOR,
            value="#7e8182",
            extra_data={
                "name": "Gray"
            },
            price=50,
        )
        Option.objects.create(
            site_configuration=site_configuration,
            type=Option.Type.DECK_COLOR,
            value="#7e8182",
            extra_data={
                "name": "Gray"
            },
            price=0
        )

        # load_initial()

        return
        # order = Order.objects.get(customer_facing_id="V47HUDBQ0N")
        #
        # api = SendgridApi()
        # refund_id = "Test Refund ID"
        # try:
        #     x = 1 / 0
        # except Exception as exc:
        #     SendgridApi().send_checkout_failed_email(order, refund_id, exc)
        #
        # return

        # api.send_submit_for_approval_email(order)
        # api.send_contact_email(
        #     name="Cedric",
        #     email="cedricholz@gmail.com",
        #     phone="12183702412",
        #     message_text="What about that mf lowercase name",
        # )

        # return
        #
        # # Order.objects.exclude(type__in=Order.Type.values).delete()
        #
        # return
        # Product.objects.filter(type=Product.Type.APPAREL).delete()
        #
        # return
        # order = Order.objects.get(customer_facing_id="Q5VFMWDR2E")
        #
        # print(order.comment.text)
        #
        # return
        # AdditionalCharge.objects.create(
        #     name="Some charge",
        #     amount=100,
        #     order=order,
        #     description="And htere's the fucking description",
        # )
        #
        #
        #
        # return

        # for option in Option.objects.filter(
        #     type=Option.Type.WIDTH_LARGE,
        # ):
        #     print(option.value)
        # return

        return
