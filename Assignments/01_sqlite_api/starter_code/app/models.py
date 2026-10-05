"""Pydantic v2 response models. Add more as you build out the phases."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    address: str
    zipcode: str
    state_code: str | None = None


class Product(BaseModel):
    product_id: int
    product_name: str
    unit_price: float


class Purchase(BaseModel):
    purchase_id: int
    customer_id: int
    product_id: int
    department: str
    amount: float
    purchase_date: date


class PurchaseDetail(BaseModel):
    purchase_id: int
    purchase_date: date
    product_name: str
    department: str
    amount: float


class RevenueRow(BaseModel):
    key: str          # state_code, month, department, ...
    num_purchases: int
    revenue: float


class NewPurchase(BaseModel):
    customer_id: int
    card_id: int
    product_id: int
    department: str
    amount: float
    purchase_date: date


class Page(BaseModel):
    """Envelope for keyset-paginated results (Phase 3)."""
    items: list
    next_cursor: int | None = None
    total: int | None = None
