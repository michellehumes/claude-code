# Sales report ingestion

This script ingests Etsy and Amazon CSV sales reports and emits a unified `profit_summary.csv` with per-order and per-day profitability metrics.

## Usage

```bash
python3 sales_reporting/ingest_sales_reports.py \
  --etsy path/to/etsy_orders.csv \
  --amazon path/to/amazon_orders.csv \
  --output profit_summary.csv
```

You can pass multiple files for each platform by repeating paths after `--etsy` or `--amazon`.

## Output columns

`profit_summary.csv` contains these columns:

| Column | Description |
| --- | --- |
| `summary_type` | `order` for per-order rows, `day` for per-day aggregates |
| `platform` | `etsy`, `amazon`, or `all` (for per-day totals) |
| `order_id` | Order identifier (blank for daily rows) |
| `order_date` | ISO date (`YYYY-MM-DD`) |
| `gross_revenue` | Total customer-facing revenue |
| `platform_fees` | Marketplace fees deducted by Etsy/Amazon |
| `estimated_shipping` | Shipping costs paid by the seller |
| `net_profit` | Gross revenue minus fees and shipping |

## Calculation logic

### Gross revenue
* **Etsy:** Uses `Order Total` (or similarly named columns such as `Total`, `Gross Sales`, `Sale Amount`).
* **Amazon:** Uses `Order Total`/`Total` when present. Otherwise, it sums `Item Total` + `Shipping Credits` + `Gift Wrap Credits`.

### Platform fees
* **Etsy:** Sums any column containing `fee` in the header (except shipping-related fees), including `Transaction Fee`, `Listing Fee`, and `Payment Processing Fee`.
* **Amazon:** Sums columns containing `fee` or `commission` (excluding shipping fees), such as `Selling Fees`, `FBA Fees`, or `Commission`.

### Estimated shipping
* **Etsy:** Uses shipping columns like `Shipping`, `Shipping Amount`, or `Shipping Cost` when provided.
* **Amazon:** Sums shipping cost columns such as `Shipping Cost`, `Shipping Chargeback`, `Shipping Label`, and `Postage`.

### Net profit
`net_profit = gross_revenue - platform_fees - estimated_shipping`

### Per-day summary
Daily rows aggregate all orders (both Etsy and Amazon) that share the same `order_date`.

## Notes
* Headers are normalized (lowercased, non-alphanumeric characters removed), so columns like `Order Total` and `order_total` map correctly.
* If a column is missing, its value defaults to `0.00`.
