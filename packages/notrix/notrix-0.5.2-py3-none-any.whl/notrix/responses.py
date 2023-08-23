class PaymentPageResponse:
    def __init__(self, uuid: str, price: float, webhook_url: str, link: str):
        self.uuid = uuid
        self.price = price
        self.webhook_url = webhook_url
        self._link = link

    def link(self, user_id: str) -> str:
        return f"{self._link}?userid={user_id}"
