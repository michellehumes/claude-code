#!/usr/bin/env python3
"""Ingest Etsy and Amazon CSV sales reports and emit profit_summary.csv."""

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class OrderRecord:
    platform: str
    order_id: str
    order_date: str
    gross_revenue: Decimal
    platform_fees: Decimal
    estimated_shipping: Decimal

    @property
    def net_profit(self) -> Decimal:
        return self.gross_revenue - self.platform_fees - self.estimated_shipping


DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
]


def normalize_header(header: str) -> str:
    return "".join(ch for ch in header.lower().strip() if ch.isalnum())


def parse_decimal(value: str) -> Decimal:
    if value is None:
        return Decimal("0")
    cleaned = value.replace("$", "").replace(",", "").strip()
    if cleaned == "":
        return Decimal("0")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return Decimal("0")


def parse_date(raw: str) -> str:
    if not raw:
        return ""
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(raw).date().isoformat()
    except ValueError:
        return raw


def get_value(row: dict, keys: Iterable[str]) -> Optional[str]:
    for key in keys:
        if key in row:
            return row[key]
    return None


def sum_columns(row: dict, keys: Iterable[str]) -> Decimal:
    total = Decimal("0")
    for key in keys:
        if key in row:
            total += parse_decimal(row[key])
    return total


def read_rows(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for raw_row in reader:
            normalized_row = {}
            for header, value in raw_row.items():
                if header is None:
                    continue
                normalized_row[normalize_header(header)] = value
            if normalized_row:
                rows.append(normalized_row)
        return rows


def parse_etsy_rows(rows: List[dict]) -> List[OrderRecord]:
    records = []
    for row in rows:
        order_id = get_value(row, ["orderid", "ordernumber", "receiptid", "transactionid"]) or ""
        order_date = parse_date(get_value(row, ["saledate", "orderdate", "date"]) or "")
        gross = parse_decimal(
            get_value(
                row,
                [
                    "ordertotal",
                    "total",
                    "grosssales",
                    "saleamount",
                    "amount",
                ],
            )
            or "0"
        )
        shipping = parse_decimal(
            get_value(
                row,
                [
                    "shipping",
                    "shippingamount",
                    "shippingprice",
                    "shippingcost",
                ],
            )
            or "0"
        )
        fee_columns = [
            key
            for key in row.keys()
            if "fee" in key and "shipping" not in key
        ]
        fees = sum_columns(row, fee_columns)
        if fees == 0:
            fees = parse_decimal(get_value(row, ["fees", "transactionfees"]) or "0")
        records.append(
            OrderRecord(
                platform="etsy",
                order_id=order_id,
                order_date=order_date,
                gross_revenue=gross,
                platform_fees=fees,
                estimated_shipping=shipping,
            )
        )
    return records


def parse_amazon_rows(rows: List[dict]) -> List[OrderRecord]:
    records = []
    for row in rows:
        order_id = get_value(row, ["amazonorderid", "orderid"]) or ""
        order_date = parse_date(get_value(row, ["purchasedate", "orderdate", "date"]) or "")

        gross = parse_decimal(
            get_value(row, ["ordertotal", "total", "grosssales", "sales"]) or "0"
        )
        if gross == 0:
            gross = sum_columns(
                row,
                [
                    "itemtotal",
                    "productsales",
                    "shippingcredits",
                    "giftwrapcredits",
                ],
            )

        shipping = sum_columns(
            row,
            [
                "shippingcost",
                "shippingchargeback",
                "shippinglabel",
                "postage",
            ],
        )

        fee_columns = [
            key
            for key in row.keys()
            if "fee" in key or "commission" in key
        ]
        fee_columns = [key for key in fee_columns if "shipping" not in key]
        fees = sum_columns(row, fee_columns)
        if fees == 0:
            fees = parse_decimal(get_value(row, ["sellingfees", "amazonfees"]) or "0")

        records.append(
            OrderRecord(
                platform="amazon",
                order_id=order_id,
                order_date=order_date,
                gross_revenue=gross,
                platform_fees=fees,
                estimated_shipping=shipping,
            )
        )
    return records


def aggregate_daily(records: List[OrderRecord]) -> List[OrderRecord]:
    totals = {}
    for record in records:
        if not record.order_date:
            continue
        day_key = record.order_date
        if day_key not in totals:
            totals[day_key] = {
                "gross": Decimal("0"),
                "fees": Decimal("0"),
                "shipping": Decimal("0"),
            }
        totals[day_key]["gross"] += record.gross_revenue
        totals[day_key]["fees"] += record.platform_fees
        totals[day_key]["shipping"] += record.estimated_shipping

    daily_records = []
    for day, values in totals.items():
        daily_records.append(
            OrderRecord(
                platform="all",
                order_id="",
                order_date=day,
                gross_revenue=values["gross"],
                platform_fees=values["fees"],
                estimated_shipping=values["shipping"],
            )
        )
    return sorted(daily_records, key=lambda record: record.order_date)


def write_summary(path: Path, orders: List[OrderRecord], daily: List[OrderRecord]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "summary_type",
                "platform",
                "order_id",
                "order_date",
                "gross_revenue",
                "platform_fees",
                "estimated_shipping",
                "net_profit",
            ]
        )
        for record in orders:
            writer.writerow(
                [
                    "order",
                    record.platform,
                    record.order_id,
                    record.order_date,
                    f"{record.gross_revenue:.2f}",
                    f"{record.platform_fees:.2f}",
                    f"{record.estimated_shipping:.2f}",
                    f"{record.net_profit:.2f}",
                ]
            )
        for record in daily:
            writer.writerow(
                [
                    "day",
                    record.platform,
                    record.order_id,
                    record.order_date,
                    f"{record.gross_revenue:.2f}",
                    f"{record.platform_fees:.2f}",
                    f"{record.estimated_shipping:.2f}",
                    f"{record.net_profit:.2f}",
                ]
            )


def load_records(paths: Iterable[Path], parser) -> List[OrderRecord]:
    records = []
    for path in paths:
        rows = read_rows(path)
        records.extend(parser(rows))
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest Etsy and Amazon sales reports and output profit_summary.csv",
    )
    parser.add_argument(
        "--etsy",
        nargs="*",
        type=Path,
        default=[],
        help="Path(s) to Etsy CSV report files",
    )
    parser.add_argument(
        "--amazon",
        nargs="*",
        type=Path,
        default=[],
        help="Path(s) to Amazon CSV report files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("profit_summary.csv"),
        help="Output CSV file path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.etsy and not args.amazon:
        raise SystemExit("Please provide at least one Etsy or Amazon report.")

    orders: List[OrderRecord] = []
    orders.extend(load_records(args.etsy, parse_etsy_rows))
    orders.extend(load_records(args.amazon, parse_amazon_rows))

    orders_sorted = sorted(
        orders,
        key=lambda record: (record.order_date, record.platform, record.order_id),
    )
    daily_records = aggregate_daily(orders_sorted)
    write_summary(args.output, orders_sorted, daily_records)


if __name__ == "__main__":
    main()
