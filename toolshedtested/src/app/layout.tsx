import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ToolShed Tested - Independent Power Tool Reviews',
  description:
    'Independent power tool reviews backed by real workshop testing. Cordless drills, saws, grinders, sanders, and more tested head-to-head. No sponsorships, no bias.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
