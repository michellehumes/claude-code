# Shelzy's Designs Order Tracking System - Setup Guide

This guide will walk you through setting up the order tracking system to pull orders from both Etsy and Amazon Seller Central, and track shipments through label creation, shipping, and delivery.

## Prerequisites

- Node.js 18 or higher
- An Etsy seller account with API access
- An Amazon Seller Central account with SP-API access

## Quick Start

1. **Install dependencies:**
   ```bash
   cd shelzys-designs/order-tracking-system
   npm install
   ```

2. **Run setup:**
   ```bash
   npm run setup
   ```
   This creates the database and copies `.env.example` to `.env`

3. **Configure your API credentials** (see below)

4. **Sync your first orders:**
   ```bash
   npm run sync
   ```

5. **View your dashboard:**
   ```bash
   npm run dashboard status
   ```

---

## Etsy API Setup

### Step 1: Create an Etsy App

1. Go to [Etsy Developers](https://www.etsy.com/developers/your-apps)
2. Click "Create a New App"
3. Fill in the details:
   - App Name: "Shelzy's Order Tracker"
   - Description: "Internal order tracking system"
4. Once created, you'll get your **API Key** (Keystring)

### Step 2: Get OAuth Credentials

Etsy uses OAuth 2.0. You'll need to:

1. Set up a redirect URI in your app settings (can be `http://localhost:3000/callback`)
2. Generate an authorization URL and complete the OAuth flow
3. Exchange the code for access and refresh tokens

**For the authorization URL:**
```
https://www.etsy.com/oauth/connect?
  response_type=code&
  redirect_uri=http://localhost:3000/callback&
  scope=transactions_r%20listings_r%20shops_r&
  client_id=YOUR_API_KEY&
  state=random_string&
  code_challenge=YOUR_CODE_CHALLENGE&
  code_challenge_method=S256
```

### Step 3: Add to .env

```env
ETSY_API_KEY=your_keystring_from_step_1
ETSY_API_SECRET=your_shared_secret
ETSY_SHOP_ID=your_shop_id
ETSY_ACCESS_TOKEN=your_oauth_access_token
ETSY_REFRESH_TOKEN=your_oauth_refresh_token
```

**Finding your Shop ID:**
- Go to your Etsy shop
- The URL will be: `https://www.etsy.com/shop/YourShopName`
- Use the API to look up your shop ID:
  ```bash
  curl "https://openapi.etsy.com/v3/application/users/me" \
    -H "x-api-key: YOUR_API_KEY" \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  ```

---

## Amazon Seller Central API Setup

### Step 1: Register as a Developer

1. Go to [Seller Central](https://sellercentral.amazon.com)
2. Navigate to **Apps & Services** > **Develop Apps**
3. Register as a developer if you haven't already

### Step 2: Create an Application

1. Click "Add new app client"
2. Fill in:
   - App name: "Shelzy's Order Tracker"
   - API Type: SP-API
   - IAM ARN: (create an IAM role first)
3. Save the **Client ID** and **Client Secret**

### Step 3: Authorize Your App

1. Go to **Apps & Services** > **Manage Your Apps**
2. Click "Authorize" on your app
3. Complete the OAuth flow to get your **Refresh Token**

### Step 4: Get AWS Credentials

The SP-API requires AWS IAM credentials:

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam)
2. Create a new IAM user with programmatic access
3. Attach the `AmazonSPAPIAccess` policy
4. Save the **Access Key ID** and **Secret Access Key**

### Step 5: Add to .env

```env
AMAZON_SELLER_ID=your_seller_id
AMAZON_MARKETPLACE_ID=ATVPDKIKX0DER
AMAZON_ACCESS_KEY=your_iam_access_key
AMAZON_SECRET_KEY=your_iam_secret_key
AMAZON_REFRESH_TOKEN=your_lwa_refresh_token
AMAZON_CLIENT_ID=your_sp_api_client_id
AMAZON_CLIENT_SECRET=your_sp_api_client_secret
AMAZON_REGION=us-east-1
```

**Common Marketplace IDs:**
- US: `ATVPDKIKX0DER`
- Canada: `A2EUQ1WTGCTBG2`
- UK: `A1F83G8C2ARO7P`
- Germany: `A1PA6795UKMFR9`

---

## Carrier Tracking Setup (Optional)

For automatic tracking updates, configure carrier APIs:

### USPS
1. Register at [USPS Web Tools](https://www.usps.com/business/web-tools-apis/)
2. Add to .env:
   ```env
   USPS_USER_ID=your_usps_user_id
   ```

### UPS
1. Register at [UPS Developer](https://www.ups.com/upsdeveloperkit)
2. Add to .env:
   ```env
   UPS_ACCESS_KEY=your_access_key
   UPS_USER_ID=your_user_id
   UPS_PASSWORD=your_password
   ```

### FedEx
1. Register at [FedEx Developer](https://developer.fedex.com)
2. Add to .env:
   ```env
   FEDEX_API_KEY=your_api_key
   FEDEX_SECRET_KEY=your_secret_key
   ```

---

## Email Notifications Setup (Optional)

To receive email notifications:

1. Use Gmail with an App Password (recommended)
2. Or use any SMTP server

### Gmail Setup
1. Enable 2FA on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Add to .env:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   NOTIFICATION_EMAIL=your_email@gmail.com
   ```

---

## Running the System

### One-Time Sync
```bash
npm run sync          # Sync all platforms
npm run sync --etsy   # Sync Etsy only
npm run sync --amazon # Sync Amazon only
npm run sync --full   # Full sync (last 90 days)
```

### Update Tracking
```bash
npm run track         # Update all shipment tracking
```

### Dashboard Commands
```bash
npm run dashboard status          # Show status summary
npm run dashboard list            # List all orders
npm run dashboard list --platform etsy  # Filter by platform
npm run dashboard order ORDER_123 # Show order details
npm run dashboard revenue         # Revenue report
npm run dashboard action          # Orders needing action
```

### Record Shipment Events
```bash
# Record a new shipping label
npm run dashboard label ORDER_123 -t TRACKING123 -c USPS

# Mark as shipped
npm run dashboard ship ORDER_123

# Mark as delivered
npm run dashboard deliver ORDER_123
```

### Run as Daemon
```bash
npm start             # Run once
npm start -- --daemon # Run continuously with scheduled syncs
```

---

## Troubleshooting

### "Etsy API Error: 401"
- Your access token may have expired
- The system will try to refresh automatically
- If it persists, regenerate your OAuth tokens

### "Amazon SP-API Error: 403"
- Check your IAM permissions
- Ensure the app is authorized in Seller Central
- Verify your refresh token is valid

### "Database locked"
- Only run one instance of the daemon at a time
- Check for zombie processes: `ps aux | grep node`

### No orders syncing
- Check your Shop ID / Seller ID is correct
- Verify you have orders in the configured time range
- Run with `--full` flag for last 90 days

---

## File Structure

```
order-tracking-system/
├── src/
│   ├── config/           # Configuration management
│   ├── integrations/     # Etsy & Amazon API clients
│   │   ├── etsy.js
│   │   └── amazon.js
│   ├── models/           # Database schema & queries
│   │   └── database.js
│   ├── services/         # Business logic
│   │   ├── order-sync.js
│   │   ├── shipment-tracking.js
│   │   └── notifications.js
│   ├── dashboard.js      # CLI interface
│   └── index.js          # Main entry point
├── scripts/              # Utility scripts
├── data/                 # SQLite database (created automatically)
├── docs/                 # Documentation
└── .env                  # Your configuration (create from .env.example)
```

---

## Support

For issues or questions, check the order tracking in action:

```bash
# Run with verbose logging
DEBUG=* npm run sync
```
