# Notrix Python SDK

This SDK is divided into two parts
#### webhook verification
will help you verify the webhook source and extract its data

#### API
helps you communicate with notrix API with type hints


## Installation
```commandline
pip install notrix
```

## Basic usage

API
```python
from notrix import Client

client = Client("NOTRIX_SECRET_KEY")
payment_page = client.create_payment_page(
    title="...",
    description="...",
    image="...",
    currency_short_name="BIT",
    price=0.013,
    wallet_address="...",
)
client.get_orders(payment_page_uuid="...")
```

Webhook
```python
from fastapi import FastAPI, Request, HttpException
from notrix import WebhookVerify

api = FastAPI()
wf = WebhookVerify("WEBHOOK_VERIFICATION_KEY")

@api.post("/notrix/webhook/")
async def payment_webhook(request: Request):
    if not wf.is_verfied(request.headers):
        raise HttpException(b"request is not verified")
```
