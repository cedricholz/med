from sendgrid import SendGridAPIClient, Mail

from api.api import Api
from med.logger import Log
from med.settings import SENDGRID_API_KEY, MAIN_EMAIL


class SendgridApi(Api):

    def __init__(self, force_dev=False, force_production=False):
        super().__init__(force_dev, force_production)
        self.sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        self.from_email = MAIN_EMAIL

    def send_email(self, to_email, subject, plain_text_content, raise_error=True, cc=None):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=plain_text_content
        )

        if cc:
            message.add_cc(cc)
        try:
            resp = self.sg.send(message)
            print(resp)
            return resp.headers.get('X-Message-Id')
        except Exception as e:
            if self.sandbox:
                print(str(e))
            else:
                if raise_error:
                    raise e

    def send_contact_email(self, name, email, phone, message_text, files=None,  raise_error=False):
        if not files:
            files = []
        subject = f"Contact from {name}"
        file_links = "\n".join([file_obj.get('url') for file_obj in files])
        message_content = message_text
        if file_links and len(file_links) > 0:
            message_content = f"{message_text}\n\nAttached Files:\n{file_links}"

        message = Mail(
            from_email=self.from_email,
            to_emails=self.from_email,
        )
        message.add_cc(email)

        message.template_id = "d-a10e4c29d1024cc5b5949ad60825b778"
        dynamic_template_data = {
            "message_text": message_content,
            "name": name,
            "phone": phone,
            "email": email,
            "subject": subject,
        }
        message.dynamic_template_data = dynamic_template_data

        try:
            self.sg.send(message)
        except Exception as exc:
            Log.error(
                "send_contact_email", exc, data={
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "message_text": message_text,
                }
            )
            if raise_error:
                raise exc

    def send_cart_checkout_success_email(self, order):
        try:
            address = order.address
            to_email = address.email
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
            )
            message.add_cc(MAIN_EMAIL)

            message.template_id = "d-e78efebe5c1d4ae59a2b60b19742b8de"

            contains_inventory = order.line_items.filter(product__isnull=False).exists()
            contains_apparel = order.line_items.filter(product_variant__isnull=False).exists()
            line_items_data = []

            inventory_item_names = []

            for line_item in order.line_items.all():
                if line_item.product:
                    inventory_item_names.append(line_item.product.name)

                line_items_data.append(
                    {
                        "name": line_item.name,
                        "image": line_item.display_image,
                        # "description": line_item.description,
                        "price": f"${line_item.price:,.2f}",
                        "quantity": line_item.quantity,
                        "total": f"${line_item.total_price:,.2f}",
                    }
                )

            inventory_items_text = ""
            if len(inventory_item_names) > 1:
                inventory_items_text = ', '.join(inventory_item_names[:-1]) + ', and ' + inventory_item_names[-1]
            elif len(inventory_item_names) > 0:
                inventory_items_text = inventory_item_names[0]

            dynamic_template_data = {
                'order_number': order.customer_facing_id,
                'first_name': address.first_name,
                'line_items': line_items_data,
                "subtotal": f"${order.subtotal_paid:,.2f}",
                "total": f"${order.total_paid:,.2f}",
                "tax": f"${order.tax_paid:,.2f}",
                'contains_inventory': contains_inventory,
                'contains_apparel': contains_apparel,
                'street1': address.street1,
                'street2': address.street2,
                'city': address.city,
                'state': address.state,
                'zip': address.zip,
                'phone': address.phone,
                'country': address.country,
                'inventory_items_text': inventory_items_text,
                'subject': f"Order Confirmation {order.customer_facing_id}",
            }

            message.dynamic_template_data = dynamic_template_data
            self.sg.send(message)
        except Exception as exc:
            Log.error(title="send_order_confirmation", exc=exc)

    def send_submit_for_approval_email(self, order, raise_error=False):
        try:
            address = order.address

            message = Mail(
                from_email=self.from_email,
                to_emails=MAIN_EMAIL,
            )
            message.add_cc(address.email)
            message.template_id = "d-9b11714eeff344dc825e8684d472cf3e"

            options_data = []

            for option in order.options.all():

                url = ""
                value = option.value

                if option.extra_data:
                    url = option.extra_data.get('url')
                    if option.extra_data.get('name'):
                        value = option.extra_data.get('name')

                options_data.append(
                    {
                        "type": option.get_type_display(),
                        "value": value,
                        "url": url,
                        "price": f"${option.price:,.2f}",
                    }
                )

            dynamic_template_data = {
                'order_number': order.customer_facing_id,
                'first_name': address.first_name,
                'full_name': address.full_name,
                'options': options_data,
                "subtotal": f"${order.balance:,.2f}",
                'phone': address.phone,
                'email': address.email,
                'subject': f"Custom Order {order.customer_facing_id} Approval Needed",
                'comment_text': order.comment.text or "",
                'attachment_files': [message_attachment.url for message_attachment in
                                     order.comment.message_attachments.all()],
                'order_url': f"https://marlin.surf/custom-surfboard-order/{order.customer_facing_id}/"
            }
            message.dynamic_template_data = dynamic_template_data
            resp = self.sg.send(message)
        except Exception as exc:
            Log.error(title="send_submit_for_approval_email", exc=exc)
            if raise_error:
                raise exc

    def send_order_approved_email(self, order, raise_error=False):
        try:
            address = order.address

            message = Mail(
                from_email=self.from_email,
                to_emails=address.email,
            )
            message.add_cc(MAIN_EMAIL)
            message.template_id = "d-19afa9d1163e497ba896226dae00b135"

            dynamic_template_data = {
                'order_number': order.customer_facing_id,
                'first_name': address.first_name,
                'full_name': address.full_name,
                'phone': address.phone,
                'email': address.email,
                'subject': f"Custom Order {order.customer_facing_id} Approved",
                'order_url': f"https://marlin.surf/custom-surfboard-order/{order.customer_facing_id}/"
            }
            message.dynamic_template_data = dynamic_template_data
            self.sg.send(message)
        except Exception as exc:
            Log.error(title="send_submit_for_approval_email", exc=exc)
            if raise_error:
                raise exc

    def send_deposit_received_email(self, order, amount_subtotal, amount_total, amount_tax, raise_error=False):
        try:
            if order.deposit_received_email_sent:
                return
            address = order.address

            message = Mail(
                from_email=self.from_email,
                to_emails=address.email,
            )
            message.add_cc(MAIN_EMAIL)
            message.template_id = "d-99d4d96db36b4d3db41aaf6a6ae0529b"

            dynamic_template_data = {
                'order_number': order.customer_facing_id,
                'first_name': address.first_name,
                'full_name': address.full_name,
                'phone': address.phone,
                'email': address.email,
                'subject': f"Custom Order {order.customer_facing_id} Deposit Received",
                'order_url': f"https://marlin.surf/custom-surfboard-order/{order.customer_facing_id}/",
                "amount_subtotal": f"${amount_subtotal:,.2f}",
                "amount_total": f"${amount_total:,.2f}",
                "amount_tax": f"${amount_tax:,.2f}",
            }

            message.dynamic_template_data = dynamic_template_data
            self.sg.send(message)
            order.deposit_received_email_sent = True
            order.save()
        except Exception as exc:
            Log.error(title="send_submit_for_approval_email", exc=exc)
            if raise_error:
                raise exc

    def send_ready_for_pickup_email(self, order, raise_error=False):
        try:

            address = order.address

            message = Mail(
                from_email=self.from_email,
                to_emails=address.email,
            )
            message.add_cc(MAIN_EMAIL)
            message.template_id = "d-5c8defb61c4f49fcacfd5b7689ea035d"

            dynamic_template_data = {
                'order_number': order.customer_facing_id,
                'first_name': address.first_name,
                'full_name': address.full_name,
                'phone': address.phone,
                'email': address.email,
                'subject': f"Custom Order {order.customer_facing_id} Ready for Pickup",
                'order_url': f"https://marlin.surf/custom-surfboard-order/{order.customer_facing_id}/"
            }
            message.dynamic_template_data = dynamic_template_data
            self.sg.send(message)
        except Exception as exc:
            Log.error(title="send_submit_for_approval_email", exc=exc)
            if raise_error:
                raise exc

    def send_balance_paid_email(self, order, amount_subtotal, amount_total, amount_tax, raise_error=False):
        try:
            address = order.address

            message = Mail(
                from_email=self.from_email,
                to_emails=address.email,
            )
            message.add_cc(MAIN_EMAIL)
            message.template_id = "d-5f68234d997c4826a5a2f6f1864c9fce"

            dynamic_template_data = {
                'order_number': order.customer_facing_id,
                'first_name': address.first_name,
                'full_name': address.full_name,
                'phone': address.phone,
                'email': address.email,
                'subject': f"Custom Order {order.customer_facing_id} Balance Paid",
                'order_url': f"https://marlin.surf/custom-surfboard-order/{order.customer_facing_id}/",
                "amount_subtotal": f"${amount_subtotal:,.2f}",
                "amount_total": f"${amount_total:,.2f}",
                "amount_tax": f"${amount_tax:,.2f}",
            }
            message.dynamic_template_data = dynamic_template_data
            self.sg.send(message)

        except Exception as exc:
            Log.error(title="send_submit_for_approval_email", exc=exc)
            if raise_error:
                raise exc

    def send_checkout_failed_email(self, order, refund_id, exc):
        order_id = None
        try:
            if order:
                order_id = order.customer_facing_id
            self.send_email(
                to_email=MAIN_EMAIL,
                subject=f"CHECKOUT FAILED: {order_id}",
                plain_text_content=f"Checkout Failed. This should never happen but if it does"
                                   f" you need to deal with this right now. Here's the order"
                                   f" id: {order_id}. And here's the stripe refund id:"
                                   f" {refund_id} And here's the error.\n\n {exc}"
            )
        except Exception as exc:
            pass

    def send_tracking_email(self, tracking):
        order = tracking.order
        address = order.address

        tracking_number = tracking.tracking_number
        tracking_carrier = tracking.carrier
        tracking_url = tracking.tracking_url

        message = Mail(
            from_email=self.from_email,
            to_emails=address.email,
        )
        message.template_id = "d-714532eb3c6e4c4382bc179b2245f7b5"

        dynamic_template_data = {
            'order_number': order.customer_facing_id,
            'first_name': order.address.first_name,
            'tracking_number': tracking_number,
            'tracking_carrier': tracking_carrier,
            'tracking_url': tracking_url,
            'subject': f"Order {order.customer_facing_id} Items Shipped",
        }
        line_items_data = []
        for line_item in tracking.line_items.all():
            line_items_data.append(
                {
                    "name": line_item.name,
                    "image": line_item.display_image,
                }
            )

        dynamic_template_data['line_items'] = line_items_data

        message.dynamic_template_data = dynamic_template_data

        if not self.sandbox:
            self.sg.send(message)