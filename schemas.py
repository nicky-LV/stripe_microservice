from pydantic import BaseModel, validator
from typing import List, Optional


class LineItem(BaseModel):
    quantity: int

    # Stripe price_id
    price: str

    @validator("quantity")
    def quantity_must_be_positive(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity must be positive")

        return quantity


class StripeProductDimensions(BaseModel):
    height: float
    length: float

    # Weight in ounces
    weight: float

    # Width in inches
    width: float

    @validator("height", "length", "weight", "width")
    def validate_fields_are_positive(cls, field_value: float):
        if field_value < 0:
            return ValueError("Dimensions of a product cannot be negative.")


class StripeProduct(BaseModel):
    id: Optional[str | int]
    name: str
    active: Optional[bool] = True
    description: Optional[str]
    metadata: Optional[dict]
    images: List[str]
    package_dimensions: Optional[StripeProductDimensions]
    shippable: Optional[bool]
    statement_descriptor: Optional[str]
    tax_code: Optional[str]
    unit_label: Optional[str]
    url: Optional[str]

    @validator("statement_descriptor")
    def validate_statement_descriptor_length(cls, value):
        if not value:
            return value

        else:
            prohibited_chars = ['<', '>', r'\\', r'"', r"'"]

            for char in prohibited_chars:
                if char in value:
                    raise ValueError(f"Product statement descriptor contains one of the following prohibited characters:"
                                     f"{prohibited_chars}")

            if len(value) > 22:
                raise ValueError("Product statement descriptor exceeds 22 characters.")

            return value