"use client";

import { useState, FormEvent } from "react";

export default function EmailSignup() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setIsError(false);

    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        setMessage("You're in! Check your inbox for your discount code.");
        setIsError(false);
        setEmail("");
      } else {
        setMessage(data.error || "Something went wrong. Please try again.");
        setIsError(true);
      }
    } catch {
      setMessage("Something went wrong. Please try again.");
      setIsError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-teal/10 py-16">
      <div className="mx-auto max-w-[600px] px-6 text-center">
        <h2 className="font-heading text-3xl font-bold text-charcoal mb-4">
          Get 15% Off Your First Order
        </h2>
        <p className="text-text-light mb-8">
          Sign up for early access to new templates, exclusive discounts, and
          planning tips delivered to your inbox.
        </p>
        {message && !isError ? (
          <p className="text-teal font-semibold text-lg bg-teal/10 rounded-lg py-4 px-6">
            {message}
          </p>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="flex flex-col sm:flex-row gap-3"
          >
            <input
              type="email"
              placeholder="Your email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="flex-1 px-4 py-3 rounded-lg border border-mid-gray text-charcoal text-sm focus:outline-none focus:ring-2 focus:ring-pink disabled:opacity-60"
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-pink hover:bg-pink-hover text-white font-heading font-semibold px-6 py-3 rounded-lg transition whitespace-nowrap disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading ? "Sending..." : "Send My Code"}
            </button>
          </form>
        )}
        {message && isError && (
          <p className="text-red-500 mt-3 text-sm">
            {message}
          </p>
        )}
      </div>
    </section>
  );
}
