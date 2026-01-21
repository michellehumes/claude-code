# Shelzy's Designs Order Tracking System

A comprehensive order tracking system that integrates with **Etsy** and **Amazon Seller Central** to automatically sync orders and track shipments through every stage: **Label Created → Shipped → Delivered**.

## Features

- **Multi-Platform Integration**: Pull orders from both Etsy and Amazon Seller Central
- **Shipment Tracking**: Track label creation, shipping, and delivery status
- **Carrier Integration**: USPS, UPS, and FedEx tracking support
- **Email Notifications**: Get notified of new orders and deliveries
- **CLI Dashboard**: View orders, track shipments, and generate reports
- **Automated Sync**: Schedule automatic order syncing and tracking updates

## Quick Start

```bash
# Install dependencies
npm install

# Set up database and configuration
npm run setup

# Edit .env with your API credentials
# Then sync your orders
npm run sync

# View the dashboard
npm run dashboard status
```

## Dashboard Commands

```bash
# Status overview
npm run dashboard status

# List orders
npm run dashboard list
npm run dashboard list --platform etsy --status shipped

# Order details
npm run dashboard order ORDER_NUMBER

# Record shipping events
npm run dashboard label ORDER_123 -t TRACKING_NUM -c USPS
npm run dashboard ship ORDER_123
npm run dashboard deliver ORDER_123

# Reports
npm run dashboard revenue --days 30
npm run dashboard action  # Orders needing attention
```

## Running Modes

```bash
# One-time sync
npm start

# Continuous daemon (syncs every 30 min, tracks every 4 hours)
npm start -- --daemon
```

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

| Variable | Description |
|----------|-------------|
| `ETSY_API_KEY` | Your Etsy API keystring |
| `ETSY_SHOP_ID` | Your Etsy shop ID |
| `ETSY_ACCESS_TOKEN` | OAuth access token |
| `AMAZON_SELLER_ID` | Your Amazon Seller ID |
| `AMAZON_CLIENT_ID` | SP-API client ID |
| `AMAZON_REFRESH_TOKEN` | LWA refresh token |

See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed setup instructions.

## Order Status Flow

```
┌─────────┐   ┌─────────┐   ┌───────────────┐   ┌─────────┐   ┌───────────┐
│ Pending │ → │  Paid   │ → │ Label Created │ → │ Shipped │ → │ Delivered │
└─────────┘   └─────────┘   └───────────────┘   └─────────┘   └───────────┘
     ↑             ↑                ↑                ↑              ↑
  Order         Payment         Create           Package        Carrier
 Received      Confirmed        Label          Picked Up      Confirmed
```

## Database

Orders and shipments are stored in a local SQLite database (`data/orders.db`). Tables include:

- `orders` - Order information from all platforms
- `shipments` - Tracking numbers and shipment status
- `tracking_events` - Detailed tracking history
- `sync_log` - Sync history and errors
- `notifications` - Sent notification log

## Requirements

- Node.js 18+
- Etsy API credentials
- Amazon SP-API credentials

## License

MIT
