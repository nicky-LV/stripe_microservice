import stripe
import os
from typing import List
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .schemas import *


# Ensure that your Stripe API key is provided via the environment variable "API_KEY".
if not os.environ["API_KEY"]:
    raise OSError("Stripe API key must be provided as the environment variable: 'API_KEY'.")

app = FastAPI()


@app.post("/create-checkout-session", response_class=RedirectResponse)
async def root(line_items: List[LineItem]):
    # Check for user-provided URLs
    if not os.environ["CHECKOUT_SUCCESS_URL"]:
        raise OSError("You must provide a checkout success URL. It must be provided as a value for the environment "
                      "variable CHECKOUT_SUCCESS_URL")

    if not os.environ["CHECKOUT_CANCEL_URL"]:
        raise OSError("You must provide a checkout cancel URL. It must be provided as a value for the environment "
                      "variable CHECKOUT_CANCEL_URL")

    try:
        # Create checkout session
        session = stripe.checkout.Session.create(line_items=line_items, mode='payment',
                                                 success_url=os.environ["CHECKOUT_SUCCESS_URL"],
                                                 cancel_url=os.environ["CHECKOUT_CANCEL_URL"])

        return session.url

    except Exception as e:
        raise e
