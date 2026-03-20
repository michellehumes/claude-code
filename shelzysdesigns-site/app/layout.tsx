import type { Metadata } from "next";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import "./globals.css";

export const metadata: Metadata = {
  title: "Shelzy's Designs | Digital Templates, Planners & Trackers",
  description:
    "Beautiful, easy-to-use digital templates, planners, and trackers for budgeting, wedding planning, business management, and more. Instant download.",
  openGraph: {
    title: "Shelzy's Designs | Digital Templates, Planners & Trackers",
    description:
      "Beautiful, easy-to-use digital templates, planners, and trackers for budgeting, wedding planning, business management, and more. Instant download.",
    type: "website",
    siteName: "Shelzy's Designs",
  },
  twitter: {
    card: "summary_large_image",
    title: "Shelzy's Designs | Digital Templates, Planners & Trackers",
    description:
      "Beautiful, easy-to-use digital templates, planners, and trackers for budgeting, wedding planning, business management, and more. Instant download.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
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
      <body className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
