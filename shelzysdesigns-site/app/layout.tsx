import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Shelzy's Designs | Digital Templates, Planners & Trackers",
  description:
    "Beautiful, functional spreadsheet templates, planners, and trackers. Instant download, works in Excel and Google Sheets.",
  openGraph: {
    title: "Shelzy's Designs | Digital Templates, Planners & Trackers",
    description:
      "Beautiful, functional spreadsheet templates, planners, and trackers. Instant download, works in Excel and Google Sheets.",
    siteName: "Shelzy's Designs",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "Shelzy's Designs | Digital Templates, Planners & Trackers",
    description:
      "Beautiful, functional spreadsheet templates, planners, and trackers. Instant download, works in Excel and Google Sheets.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
