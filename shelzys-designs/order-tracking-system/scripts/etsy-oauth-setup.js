#!/usr/bin/env node

/**
 * Etsy OAuth Setup Helper for Shelzy's Designs
 *
 * Run this script to generate your OAuth tokens:
 *   node scripts/etsy-oauth-setup.js
 */

import http from 'http';
import crypto from 'crypto';
import { URL } from 'url';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function question(prompt) {
  return new Promise(resolve => rl.question(prompt, resolve));
}

// Generate PKCE code verifier and challenge
function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
  return { verifier, challenge };
}

async function main() {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║           Etsy OAuth Setup for Shelzy's Designs              ║
╚══════════════════════════════════════════════════════════════╝
`);

  // Get API key from user
  const apiKey = await question('Enter your Etsy API Key (Keystring): ');

  if (!apiKey || apiKey.length < 10) {
    console.log('\\n❌ Invalid API key. Get it from https://www.etsy.com/developers/your-apps');
    process.exit(1);
  }

  // Generate PKCE
  const { verifier, challenge } = generatePKCE();
  const state = crypto.randomBytes(16).toString('hex');

  // Scopes we need
  const scopes = [
    'transactions_r',  // Read transactions/orders
    'listings_r',      // Read listings
    'shops_r',         // Read shop info
  ].join('%20');

  const redirectUri = 'http://localhost:3456/callback';

  // Build authorization URL
  const authUrl = `https://www.etsy.com/oauth/connect?` +
    `response_type=code&` +
    `redirect_uri=${encodeURIComponent(redirectUri)}&` +
    `scope=${scopes}&` +
    `client_id=${apiKey}&` +
    `state=${state}&` +
    `code_challenge=${challenge}&` +
    `code_challenge_method=S256`;

  console.log('\\n📋 Step 1: Open this URL in your browser:\\n');
  console.log('─'.repeat(70));
  console.log(authUrl);
  console.log('─'.repeat(70));

  console.log('\\n⏳ Step 2: Waiting for authorization...');
  console.log('   (A local server is listening on port 3456)\\n');

  // Start local server to catch the callback
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://localhost:3456`);

    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');
      const returnedState = url.searchParams.get('state');

      if (returnedState !== state) {
        res.writeHead(400);
        res.end('State mismatch - possible CSRF attack');
        return;
      }

      if (!code) {
        res.writeHead(400);
        res.end('No authorization code received');
        return;
      }

      // Exchange code for tokens
      console.log('\\n✓ Authorization code received! Exchanging for tokens...');

      try {
        const tokenResponse = await fetch('https://api.etsy.com/v3/public/oauth/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            grant_type: 'authorization_code',
            client_id: apiKey,
            redirect_uri: redirectUri,
            code: code,
            code_verifier: verifier,
          }),
        });

        if (!tokenResponse.ok) {
          const error = await tokenResponse.text();
          throw new Error(`Token exchange failed: ${error}`);
        }

        const tokens = await tokenResponse.json();

        // Success page
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`
          <html>
            <body style="font-family: Arial; padding: 40px; text-align: center;">
              <h1>✅ Success!</h1>
              <p>Your Etsy OAuth tokens have been generated.</p>
              <p>You can close this window and return to the terminal.</p>
            </body>
          </html>
        `);

        // Display tokens
        console.log('\\n' + '═'.repeat(70));
        console.log('  ✅ SUCCESS! Add these to your .env file:');
        console.log('═'.repeat(70));
        console.log(`
ETSY_API_KEY=${apiKey}
ETSY_ACCESS_TOKEN=${tokens.access_token}
ETSY_REFRESH_TOKEN=${tokens.refresh_token}
`);
        console.log('═'.repeat(70));
        console.log('\\n⚠️  IMPORTANT: The access token expires in 1 hour.');
        console.log('   The refresh token expires in 90 days.');
        console.log('   The system will auto-refresh tokens when needed.\\n');

        // Now get shop info
        console.log('Fetching your shop information...');

        try {
          const meResponse = await fetch('https://openapi.etsy.com/v3/application/users/me', {
            headers: {
              'x-api-key': apiKey,
              'Authorization': `Bearer ${tokens.access_token}`,
            },
          });

          if (meResponse.ok) {
            const userData = await meResponse.json();
            console.log(`\\nUser ID: ${userData.user_id}`);
            console.log(`Shop ID: ${userData.shop_id || 'No shop found'}`);

            if (userData.shop_id) {
              console.log(`\\nAdd this to your .env file:`);
              console.log(`ETSY_SHOP_ID=${userData.shop_id}`);
            }
          }
        } catch (e) {
          console.log('Could not fetch shop info:', e.message);
        }

        server.close();
        rl.close();
        process.exit(0);

      } catch (error) {
        res.writeHead(500);
        res.end(`Error: ${error.message}`);
        console.error('\\n❌ Token exchange failed:', error.message);
        server.close();
        rl.close();
        process.exit(1);
      }
    }
  });

  server.listen(3456, () => {
    console.log('Local server started on http://localhost:3456');
  });

  // Timeout after 5 minutes
  setTimeout(() => {
    console.log('\\n⏰ Timeout - no authorization received after 5 minutes.');
    server.close();
    rl.close();
    process.exit(1);
  }, 5 * 60 * 1000);
}

main().catch(console.error);
