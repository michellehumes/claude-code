import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';

export const metadata: Metadata = {
  title: 'WealthNexus - Next-Generation Wealth Management',
  description: 'Enterprise-grade portfolio management, analytics, and reporting for wealth advisors.',
  keywords: ['wealth management', 'portfolio management', 'RIA', 'financial advisor', 'investment management'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
