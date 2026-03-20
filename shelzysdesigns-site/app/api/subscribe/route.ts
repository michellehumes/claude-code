import { NextRequest, NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

const SUBSCRIBERS_FILE = path.join(process.cwd(), "subscribers.json");

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email } = body;

    if (!email || typeof email !== "string") {
      return NextResponse.json(
        { error: "Email is required." },
        { status: 400 }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: "Please enter a valid email address." },
        { status: 400 }
      );
    }

    // Read existing subscribers
    let subscribers: string[] = [];
    try {
      const data = await fs.readFile(SUBSCRIBERS_FILE, "utf-8");
      subscribers = JSON.parse(data);
    } catch {
      // File doesn't exist yet, start with empty array
    }

    // Check for duplicates
    if (subscribers.includes(email.toLowerCase())) {
      return NextResponse.json(
        { success: true, message: "You're already subscribed!" }
      );
    }

    // Add new subscriber
    subscribers.push(email.toLowerCase());
    await fs.writeFile(SUBSCRIBERS_FILE, JSON.stringify(subscribers, null, 2));

    console.log(`New subscriber: ${email}`);

    return NextResponse.json({
      success: true,
      message: "Successfully subscribed!",
    });
  } catch {
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
