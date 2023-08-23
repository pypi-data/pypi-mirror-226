from typing import BinaryIO

import requests
from .responses import PaymentPageResponse


class Client:
    BASE_URL = "https://notrix.io"

    def __init__(self, secret_api_key: str):
        self.secret_api_key = secret_api_key

    def _auth_headers(self) -> dict:
        return {f"Authorization": f"Token {self.secret_api_key}"}

    def _make_request(self, method: str, path: str, **kwargs):
        request_path = f"{self.BASE_URL}/{path}"
        headers = kwargs.pop("headers", {}).update(self._auth_headers())
        return requests.request(method, request_path, headers=headers, **kwargs)

    def create_payment_page(
        self, title: str, description: str, image: BinaryIO, price: float, webhook_url: str = None
    ):
        if webhook_url is None:
            webhook_url = ""

        response = self._make_request(
            "post",
            "api/payment-page/",
            data={
                "title": title,
                "description": description,
                "price": price,
                "webhook_url": webhook_url,
            },
            files={"image": image},
        )

        response.raise_for_status()

        return PaymentPageResponse(**response.json())
