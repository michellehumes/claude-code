export default () => ({
  // Server
  port: parseInt(process.env.PORT, 10) || 3001,
  nodeEnv: process.env.NODE_ENV || 'development',

  // Database
  database: {
    url: process.env.DATABASE_URL,
  },

  // Redis
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT, 10) || 6379,
    password: process.env.REDIS_PASSWORD,
  },

  // JWT
  jwt: {
    secret: process.env.JWT_SECRET || 'development-secret-change-in-production',
    expiresIn: process.env.JWT_EXPIRES_IN || '1d',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d',
  },

  // AWS
  aws: {
    region: process.env.AWS_REGION || 'us-east-1',
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    s3Bucket: process.env.AWS_S3_BUCKET,
  },

  // CORS
  cors: {
    origins: process.env.CORS_ORIGINS || 'http://localhost:3000',
  },

  // Rate Limiting
  throttle: {
    ttl: parseInt(process.env.THROTTLE_TTL, 10) || 60000,
    limit: parseInt(process.env.THROTTLE_LIMIT, 10) || 100,
  },

  // Email
  email: {
    from: process.env.EMAIL_FROM || 'noreply@wealthnexus.io',
    smtpHost: process.env.SMTP_HOST,
    smtpPort: parseInt(process.env.SMTP_PORT, 10) || 587,
    smtpUser: process.env.SMTP_USER,
    smtpPass: process.env.SMTP_PASS,
  },

  // External Services
  services: {
    plaidClientId: process.env.PLAID_CLIENT_ID,
    plaidSecret: process.env.PLAID_SECRET,
    plaidEnv: process.env.PLAID_ENV || 'sandbox',
  },
});
