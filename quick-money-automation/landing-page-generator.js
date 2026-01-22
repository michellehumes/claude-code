#!/usr/bin/env node

/**
 * INSTANT LANDING PAGE GENERATOR
 *
 * Creates a simple, converting landing page in 5 minutes
 * Perfect for product launches, services, or lead capture
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => {
    rl.question(question, answer => {
      resolve(answer);
    });
  });
}

async function main() {
  console.log('\n💻 INSTANT LANDING PAGE GENERATOR\n');
  console.log('Create a converting landing page in 5 minutes\n');

  // Gather info
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 1: Page Information');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const productName = await ask('Product/Service name: ');
  const headline = await ask('Main headline (the big promise): ');
  const subheadline = await ask('Subheadline (supporting text): ');
  const price = await ask('Price: $');
  const cta = await ask('Call-to-action button text (e.g., "Buy Now", "Get Started"): ');
  const paymentLink = await ask('Payment link (Gumroad, Stripe, PayPal, etc.): ');

  // Benefits
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('STEP 2: Benefits (What they get)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  const benefits = [];
  for (let i = 1; i <= 5; i++) {
    const benefit = await ask(`Benefit ${i} (or press Enter to skip): `);
    if (benefit.trim()) benefits.push(benefit);
  }

  // Generate HTML
  const html = generateLandingPage({
    productName,
    headline,
    subheadline,
    price,
    cta,
    paymentLink,
    benefits
  });

  // Save file
  const outputDir = path.join(process.cwd(), 'landing-pages');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const fileName = productName.toLowerCase().replace(/[^a-z0-9]/g, '-') + '.html';
  const filePath = path.join(outputDir, fileName);

  fs.writeFileSync(filePath, html);

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✅ LANDING PAGE CREATED!');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log(`File saved to: ${filePath}\n`);

  console.log('NEXT STEPS:\n');
  console.log('1. Open the file in your browser to preview');
  console.log('2. Customize colors/images if needed');
  console.log('3. Deploy to:');
  console.log('   • Netlify Drop (drag & drop) - FREE');
  console.log('   • Vercel (drag & drop) - FREE');
  console.log('   • GitHub Pages - FREE');
  console.log('   • Surge.sh (command: surge ' + filePath + ') - FREE');
  console.log('\n4. Share your link everywhere!\n');

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🚀 DEPLOYMENT OPTIONS');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log('FASTEST (1 minute):');
  console.log('1. Go to: https://app.netlify.com/drop');
  console.log('2. Drag your HTML file');
  console.log('3. Get instant live URL\n');

  console.log('OR use Surge (command line):');
  console.log('$ npm install -g surge');
  console.log(`$ surge ${filePath}\n`);

  console.log('Your page is ready to make money! 💰\n');

  rl.close();
}

function generateLandingPage({ productName, headline, subheadline, price, cta, paymentLink, benefits }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${productName} - ${headline}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: #1a1a1a;
            line-height: 1.2;
        }

        .subheadline {
            font-size: 1.3em;
            color: #666;
            margin-bottom: 40px;
        }

        .benefits {
            margin: 40px 0;
        }

        .benefit {
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: transform 0.2s;
        }

        .benefit:hover {
            transform: translateX(5px);
        }

        .benefit-icon {
            font-size: 24px;
            margin-right: 15px;
            flex-shrink: 0;
        }

        .benefit-text {
            font-size: 1.1em;
            color: #333;
        }

        .price-section {
            text-align: center;
            margin: 50px 0;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
        }

        .price {
            font-size: 3.5em;
            font-weight: bold;
            margin: 20px 0;
        }

        .price-label {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .cta-button {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 20px 60px;
            font-size: 1.3em;
            font-weight: bold;
            text-decoration: none;
            border-radius: 50px;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
            margin-top: 20px;
        }

        .cta-button:hover {
            background: #059669;
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(16, 185, 129, 0.4);
        }

        .urgency {
            text-align: center;
            color: #dc2626;
            font-weight: bold;
            margin: 30px 0;
            font-size: 1.1em;
        }

        .guarantee {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: #fef3c7;
            border-radius: 10px;
            border: 2px dashed #f59e0b;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            color: #666;
            font-size: 0.9em;
        }

        @media (max-width: 768px) {
            .container {
                padding: 40px 20px;
            }

            h1 {
                font-size: 2em;
            }

            .price {
                font-size: 2.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>${headline}</h1>
        <p class="subheadline">${subheadline}</p>

        <div class="benefits">
            <h2 style="margin-bottom: 25px; font-size: 1.8em;">What You Get:</h2>
            ${benefits.map(benefit => `
            <div class="benefit">
                <span class="benefit-icon">✓</span>
                <span class="benefit-text">${benefit}</span>
            </div>
            `).join('')}
        </div>

        <div class="price-section">
            <p class="price-label">Get instant access for:</p>
            <div class="price">$${price}</div>
            <a href="${paymentLink}" class="cta-button">${cta}</a>
        </div>

        <p class="urgency">⚡ Limited time offer - Price goes up soon!</p>

        <div class="guarantee">
            <strong>💯 100% Satisfaction Guaranteed</strong>
            <p style="margin-top: 10px;">If you're not happy, get a full refund. No questions asked.</p>
        </div>

        <div class="footer">
            <p>${productName} © ${new Date().getFullYear()}</p>
            <p style="margin-top: 10px;">Questions? Email: your@email.com</p>
        </div>
    </div>

    <!-- Simple analytics (optional) -->
    <script>
        // Track button clicks
        document.querySelector('.cta-button').addEventListener('click', function() {
            console.log('CTA clicked!');
            // Add analytics tracking here if needed
        });
    </script>
</body>
</html>`;
}

main().catch(console.error);
