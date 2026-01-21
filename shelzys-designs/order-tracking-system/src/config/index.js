import { config as dotenvConfig } from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables
dotenvConfig({ path: join(__dirname, '../../.env') });

export const config = {
  // Etsy Configuration
  etsy: {
    apiKey: process.env.ETSY_API_KEY,
    apiSecret: process.env.ETSY_API_SECRET,
    shopId: process.env.ETSY_SHOP_ID,
    accessToken: process.env.ETSY_ACCESS_TOKEN,
    refreshToken: process.env.ETSY_REFRESH_TOKEN,
    baseUrl: 'https://openapi.etsy.com/v3',
  },

  // Amazon Seller Central Configuration
  amazon: {
    sellerId: process.env.AMAZON_SELLER_ID,
    marketplaceId: process.env.AMAZON_MARKETPLACE_ID || 'ATVPDKIKX0DER',
    accessKey: process.env.AMAZON_ACCESS_KEY,
    secretKey: process.env.AMAZON_SECRET_KEY,
    refreshToken: process.env.AMAZON_REFRESH_TOKEN,
    clientId: process.env.AMAZON_CLIENT_ID,
    clientSecret: process.env.AMAZON_CLIENT_SECRET,
    region: process.env.AMAZON_REGION || 'us-east-1',
    baseUrl: 'https://sellingpartnerapi-na.amazon.com',
  },

  // Carrier Tracking APIs
  carriers: {
    usps: {
      userId: process.env.USPS_USER_ID,
    },
    ups: {
      accessKey: process.env.UPS_ACCESS_KEY,
      userId: process.env.UPS_USER_ID,
      password: process.env.UPS_PASSWORD,
    },
    fedex: {
      apiKey: process.env.FEDEX_API_KEY,
      secretKey: process.env.FEDEX_SECRET_KEY,
    },
  },

  // Email Configuration
  email: {
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port: parseInt(process.env.SMTP_PORT) || 587,
    user: process.env.SMTP_USER,
    password: process.env.SMTP_PASSWORD,
    notificationEmail: process.env.NOTIFICATION_EMAIL,
  },

  // Application Settings
  app: {
    databasePath: process.env.DATABASE_PATH || './data/orders.db',
    syncIntervalMinutes: parseInt(process.env.SYNC_INTERVAL_MINUTES) || 30,
    trackingCheckIntervalHours: parseInt(process.env.TRACKING_CHECK_INTERVAL_HOURS) || 4,
    logLevel: process.env.LOG_LEVEL || 'info',
  },
};

// Validation helper
export function validateConfig(platform) {
  const required = {
    etsy: ['apiKey', 'shopId', 'accessToken'],
    amazon: ['sellerId', 'refreshToken', 'clientId', 'clientSecret'],
  };

  if (platform && required[platform]) {
    const missing = required[platform].filter(key => !config[platform][key]);
    if (missing.length > 0) {
      throw new Error(`Missing ${platform} configuration: ${missing.join(', ')}`);
    }
  }

  return true;
}

export default config;
