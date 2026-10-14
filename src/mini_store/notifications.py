"""Customer notification behavior."""

""" To refactor this code, i am going to decouple the sender logic from each function"""

class emailSender:
    def __init__(self, email_sender):
            self.email_sender = email_sender

    def send_order_confirmation(self, customer, order_id: str) -> None:
        subject = f"Order {order_id} confirmed"
        message = f"Hello {customer.name}, your order {order_id} was confirmed."
        self.email_sender.send(customer.email, subject, message)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        subject = f"Order {order_id} shipped"
        message = (
            f"Hello {customer.name}, your order {order_id} shipped. "
            f"Tracking: {tracking_code}."
        )
        self.email_sender.send(customer.email, subject, message)

class smsSender:
    def __init__(self, sms_sender):
            self.sms_sender = sms_sender

    def send_order_confirmation(self, customer, order_id: str) -> None:
        message = f"Order {order_id} confirmed for {customer.name}."
        self.sms_sender.send(customer.phone, message)

    def send_shipping_update(
        self, customer, order_id: str, tracking_code: str
    ) -> None:
        message = f"Order {order_id} shipped. Tracking: {tracking_code}."
        self.sms_sender.send(customer.phone, message)

class pushSender:
    def __init__(self, push_sender):
        self.push_sender = push_sender
    
    def send_order_confirmation(self, customer, order_id: str) -> None:
        title = "Order confirmed"
        message = f"Order {order_id} is confirmed."
        self.push_sender.send(customer.device_id, title, message)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        title = "Order shipped"
        message = f"Track order {order_id}: {tracking_code}."
        self.push_sender.send(customer.device_id, title, message)

class NotificationService:
    def __init__(self, email_sender, sms_sender, push_sender):
        "I prefer a dictionary instead of an if else statement to decouple even more the notification logic"
        self.channels = {
            "email": emailSender(email_sender),
            "sms": smsSender(sms_sender),
            "push": pushSender(push_sender),
        }

    def getPrferredChannel(self, customer):
        channel = self.channels.get(customer.preferred_channel)

        if channel is None:
            raise ValueError("Unsupported notification channel")

        return channel

    def send_order_confirmation(self, customer, order_id: str) -> None:
        self.getPrferredChannel(customer).send_order_confirmation(customer, order_id)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        self.getPrferredChannel(customer).send_shipping_update( customer, order_id, tracking_code)