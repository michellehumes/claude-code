"use client";

import { useState } from "react";
import { siteConfig } from "@/site.config";

export function Newsletter() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");

    // Placeholder for newsletter signup logic
    // Replace with actual integration (Mailchimp, ConvertKit, etc.)
    setTimeout(() => {
      setStatus("success");
      setEmail("");
    }, 1000);
  };

  return (
    <section className="rounded-2xl bg-gradient-to-br from-pink-500 to-purple-600 p-8 text-white md:p-12">
      <div className="mx-auto max-w-2xl text-center">
        {/* Icon */}
        <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-full bg-white/20">
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>

        {/* Heading */}
        <h2 className="text-2xl font-bold md:text-3xl">
          Get the Latest Beauty Drops
        </h2>
        <p className="mt-3 text-pink-100">
          Subscribe to {siteConfig.name} for weekly beauty tips, product picks, and
          trend alerts delivered straight to your inbox.
        </p>

        {/* Form */}
        {status === "success" ? (
          <div className="mt-6 rounded-lg bg-white/20 p-4">
            <p className="font-medium">
              You&apos;re in! Check your inbox to confirm your subscription.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-6">
            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                className="flex-grow rounded-lg border-0 bg-white/20 px-4 py-3 text-white placeholder-white/70 backdrop-blur focus:outline-none focus:ring-2 focus:ring-white/50"
              />
              <button
                type="submit"
                disabled={status === "loading"}
                className="rounded-lg bg-white px-6 py-3 font-semibold text-pink-600 transition-colors hover:bg-pink-50 disabled:opacity-70"
              >
                {status === "loading" ? "Subscribing..." : "Subscribe"}
              </button>
            </div>
            <p className="mt-3 text-xs text-pink-200">
              No spam, ever. Unsubscribe anytime.
            </p>
          </form>
        )}
      </div>
    </section>
  );
}

export default Newsletter;
