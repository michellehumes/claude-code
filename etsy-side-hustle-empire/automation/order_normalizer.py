#!/usr/bin/env python3
"""
Normalize Etsy and Amazon order CSV exports into a single production-tracking format.

Usage:
  python order_normalizer.py --etsy path/to/etsy.csv --amazon path/to/amazon.csv -o normalized.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, List, Dict, Optional


NORMALIZED_FIELDS = [
    "order_id",
    "order_date",
    "platform",
    "order_status",
    "fulfillment_status",
    "buyer_name",
    "buyer_email",
    "item_name",
    "sku",
    "quantity",
    "item_price",
    "shipping_price",
    "tax",
    "total",
    "currency",
    "shipping_name",
    "shipping_address_1",
    "shipping_address_2",
    "shipping_city",
    "shipping_state",
    "shipping_postal_code",
    "shipping_country",
    "notes",
]


def normalize_header(header: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", header.strip().lower())


def get_value(row: Dict[str, str], candidates: Iterable[str]) -> str:
    normalized_row = {normalize_header(key): value for key, value in row.items()}
    for candidate in candidates:
        normalized_candidate = normalize_header(candidate)
        if normalized_candidate in normalized_row:
            return normalized_row[normalized_candidate].strip()
    return ""


def parse_decimal(value: str) -> Optional[Decimal]:
    if not value:
        return None
    cleaned = value.strip()
    cleaned = cleaned.replace(",", "")
    cleaned = re.sub(r"^\((.*)\)$", r"-\1", cleaned)
    cleaned = re.sub(r"[^0-9.\-]", "", cleaned)
    if cleaned in {"", "-", ".", "-."}:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def parse_date(value: str) -> str:
    if not value:
        return ""
    cleaned = value.strip()
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for fmt in formats:
        try:
            parsed = dt.datetime.strptime(cleaned, fmt)
            return parsed.date().isoformat()
        except ValueError:
            continue
    return cleaned


def decimal_to_str(value: Optional[Decimal]) -> str:
    if value is None:
        return ""
    return f"{value:.2f}"


def normalize_etsy_row(row: Dict[str, str]) -> Dict[str, str]:
    order_id = get_value(row, ["Order ID", "Order Number", "Receipt ID"])
    order_date = parse_date(get_value(row, ["Order Date", "Date", "Sale Date"]))
    buyer_name = get_value(row, ["Buyer", "Buyer Name", "Name"])
    buyer_email = get_value(row, ["Buyer Email", "Email"])
    item_name = get_value(row, ["Item Name", "Listing Title", "Product"])
    sku = get_value(row, ["SKU", "Listing SKU"])
    quantity = get_value(row, ["Quantity", "Qty"])
    item_price = parse_decimal(get_value(row, ["Item Price", "Item Total", "Price"]))
    shipping_price = parse_decimal(get_value(row, ["Shipping", "Shipping Price"]))
    tax = parse_decimal(get_value(row, ["Sales Tax", "Tax"]))
    total = parse_decimal(get_value(row, ["Order Total", "Total", "Grand Total"]))
    currency = get_value(row, ["Currency", "Order Currency"])
    order_status = get_value(row, ["Order Status", "Status"])
    fulfillment_status = get_value(row, ["Fulfillment Status", "Shipping Status"])

    shipping_name = get_value(row, ["Ship Name", "Shipping Name"])
    shipping_address_1 = get_value(row, ["Ship Address1", "Shipping Address 1"])
    shipping_address_2 = get_value(row, ["Ship Address2", "Shipping Address 2"])
    shipping_city = get_value(row, ["Ship City", "Shipping City"])
    shipping_state = get_value(row, ["Ship State", "Shipping State", "Ship Province"])
    shipping_postal_code = get_value(row, ["Ship Postal Code", "Shipping Postal Code", "Zip"])
    shipping_country = get_value(row, ["Ship Country", "Shipping Country"])

    quantity_value = str(int(quantity)) if quantity.isdigit() else quantity

    if total is None:
        qty = Decimal(quantity_value) if quantity_value and quantity_value.isdigit() else Decimal(1)
        item_total = item_price * qty if item_price is not None else Decimal(0)
        total = item_total + (shipping_price or Decimal(0)) + (tax or Decimal(0))

    return {
        "order_id": order_id,
        "order_date": order_date,
        "platform": "Etsy",
        "order_status": order_status,
        "fulfillment_status": fulfillment_status,
        "buyer_name": buyer_name,
        "buyer_email": buyer_email,
        "item_name": item_name,
        "sku": sku,
        "quantity": quantity_value,
        "item_price": decimal_to_str(item_price),
        "shipping_price": decimal_to_str(shipping_price),
        "tax": decimal_to_str(tax),
        "total": decimal_to_str(total),
        "currency": currency,
        "shipping_name": shipping_name,
        "shipping_address_1": shipping_address_1,
        "shipping_address_2": shipping_address_2,
        "shipping_city": shipping_city,
        "shipping_state": shipping_state,
        "shipping_postal_code": shipping_postal_code,
        "shipping_country": shipping_country,
        "notes": "",
    }


def normalize_amazon_row(row: Dict[str, str]) -> Dict[str, str]:
    order_id = get_value(row, ["order-id", "Order ID"])
    order_date = parse_date(get_value(row, ["purchase-date", "Order Date"]))
    buyer_name = get_value(row, ["buyer-name", "Buyer Name"])
    buyer_email = get_value(row, ["buyer-email", "Buyer Email"])
    item_name = get_value(row, ["product-name", "Item Name"])
    sku = get_value(row, ["sku", "Seller SKU"])
    quantity = get_value(row, ["quantity-purchased", "Quantity"])
    item_price = parse_decimal(get_value(row, ["item-price", "Item Price"]))
    shipping_price = parse_decimal(get_value(row, ["shipping-price", "Shipping Price"]))
    item_tax = parse_decimal(get_value(row, ["item-tax", "Item Tax"]))
    shipping_tax = parse_decimal(get_value(row, ["shipping-tax", "Shipping Tax"]))
    tax = None
    if item_tax or shipping_tax:
        tax = (item_tax or Decimal(0)) + (shipping_tax or Decimal(0))
    total = parse_decimal(get_value(row, ["order-item-total", "Order Total", "Total"]))
    currency = get_value(row, ["currency", "Currency"])
    order_status = get_value(row, ["order-status", "Order Status"])
    fulfillment_status = get_value(row, ["fulfillment-channel", "Fulfillment Channel"])

    shipping_name = get_value(row, ["ship-name", "Shipping Name"])
    shipping_address_1 = get_value(row, ["ship-address-1", "Shipping Address 1"])
    shipping_address_2 = get_value(row, ["ship-address-2", "Shipping Address 2"])
    shipping_city = get_value(row, ["ship-city", "Shipping City"])
    shipping_state = get_value(row, ["ship-state", "Shipping State"])
    shipping_postal_code = get_value(row, ["ship-postal-code", "Shipping Postal Code"])
    shipping_country = get_value(row, ["ship-country", "Shipping Country"])

    quantity_value = str(int(quantity)) if quantity.isdigit() else quantity

    if total is None:
        qty = Decimal(quantity_value) if quantity_value and quantity_value.isdigit() else Decimal(1)
        item_total = item_price * qty if item_price is not None else Decimal(0)
        total = item_total + (shipping_price or Decimal(0)) + (tax or Decimal(0))

    return {
        "order_id": order_id,
        "order_date": order_date,
        "platform": "Amazon",
        "order_status": order_status,
        "fulfillment_status": fulfillment_status,
        "buyer_name": buyer_name,
        "buyer_email": buyer_email,
        "item_name": item_name,
        "sku": sku,
        "quantity": quantity_value,
        "item_price": decimal_to_str(item_price),
        "shipping_price": decimal_to_str(shipping_price),
        "tax": decimal_to_str(tax),
        "total": decimal_to_str(total),
        "currency": currency,
        "shipping_name": shipping_name,
        "shipping_address_1": shipping_address_1,
        "shipping_address_2": shipping_address_2,
        "shipping_city": shipping_city,
        "shipping_state": shipping_state,
        "shipping_postal_code": shipping_postal_code,
        "shipping_country": shipping_country,
        "notes": "",
    }


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def normalize_files(paths: Iterable[Path], platform: str) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for path in paths:
        for row in load_rows(path):
            if platform == "etsy":
                normalized.append(normalize_etsy_row(row))
            elif platform == "amazon":
                normalized.append(normalize_amazon_row(row))
    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize Etsy and Amazon order CSVs into a unified production-tracking CSV."
    )
    parser.add_argument("--etsy", nargs="*", default=[], help="Path(s) to Etsy CSV exports.")
    parser.add_argument("--amazon", nargs="*", default=[], help="Path(s) to Amazon CSV exports.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    etsy_paths = [Path(p) for p in args.etsy]
    amazon_paths = [Path(p) for p in args.amazon]

    if not etsy_paths and not amazon_paths:
        raise SystemExit("Provide at least one Etsy or Amazon CSV via --etsy or --amazon.")

    rows: List[Dict[str, str]] = []
    rows.extend(normalize_files(etsy_paths, "etsy"))
    rows.extend(normalize_files(amazon_paths, "amazon"))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=NORMALIZED_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in NORMALIZED_FIELDS})


if __name__ == "__main__":
    main()
