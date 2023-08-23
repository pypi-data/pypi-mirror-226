# Notrix Python SDK

## Installation
```commandline
pip install notrix
```

## Basic usage

```python
from notrix import Client

client = Client("NOTRIX_SECRET_KEY")
payment_page = client.create_payment_page(
    title="Bike",
    description="My amazing bike",
    image=open("bike.png", 'rb'),
    price=1.5,  # USD,
    webhook_url="https://example.com/webhooks/notrix/"
)

print(payment_page.link)  # Payment link for users
print(payment_page.price)  # The price in USD
print(payment_page.webhook_url) 
print(payment_page.uuid)
```
