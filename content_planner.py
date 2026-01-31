#!/usr/bin/env python3
"""Generate a 30-day social content calendar CSV.

The calendar balances product launches, promotions, and evergreen posts with
platform-optimized formats for Instagram, TikTok, Pinterest, and Facebook.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
from pathlib import Path
from typing import Dict, List, Optional


PLATFORMS = ["Instagram", "TikTok", "Pinterest", "Facebook"]

FORMAT_ROTATION = {
    "Instagram": {
        "launch": ["Reel", "Carousel", "Story"],
        "promo": ["Story", "Reel", "Carousel"],
        "evergreen": ["Carousel", "Reel", "Story"],
    },
    "TikTok": {
        "launch": ["Short video", "Product demo"],
        "promo": ["Short video", "Offer reminder"],
        "evergreen": ["Short video", "Trend remix"],
    },
    "Pinterest": {
        "launch": ["Idea Pin", "Product Pin"],
        "promo": ["Product Pin", "Idea Pin"],
        "evergreen": ["Idea Pin", "Infographic Pin"],
    },
    "Facebook": {
        "launch": ["Video", "Photo", "Event"],
        "promo": ["Photo", "Video", "Link"],
        "evergreen": ["Photo", "Video", "Link"],
    },
}

ANGLE_BY_PHASE = {
    "launch_teaser": "Teaser",
    "launch_countdown": "Countdown",
    "launch_day": "Launch announcement",
    "launch_followup": "Demo/FAQ",
    "promo_start": "Offer kickoff",
    "promo_mid": "Offer reminder",
    "promo_end": "Last chance",
    "evergreen": "Evergreen value",
}

CTA_BY_TYPE = {
    "launch": "Learn more",
    "promo": "Shop offer",
    "evergreen": "Save/Bookmark",
}


@dataclasses.dataclass
class Launch:
    date: dt.date
    product: str


@dataclasses.dataclass
class Promotion:
    start_date: dt.date
    end_date: dt.date
    name: str


@dataclasses.dataclass
class Config:
    start_date: dt.date
    launches: List[Launch]
    promotions: List[Promotion]
    evergreen_topics: List[str]


def parse_date(value: str) -> dt.date:
    return dt.datetime.strptime(value, "%Y-%m-%d").date()


def load_config(path: Path) -> Config:
    data = json.loads(path.read_text())
    start_date = parse_date(data["start_date"])
    launches = [Launch(parse_date(item["date"]), item["product"]) for item in data.get("launches", [])]
    promotions = [
        Promotion(parse_date(item["start_date"]), parse_date(item["end_date"]), item["name"])
        for item in data.get("promotions", [])
    ]
    evergreen_topics = data.get("evergreen_topics", [])
    if not evergreen_topics:
        evergreen_topics = ["Product education", "Behind-the-scenes", "Customer proof", "Tips & tricks"]
    return Config(start_date=start_date, launches=launches, promotions=promotions, evergreen_topics=evergreen_topics)


def write_template(path: Path) -> None:
    template = {
        "start_date": dt.date.today().isoformat(),
        "launches": [
            {"date": (dt.date.today() + dt.timedelta(days=7)).isoformat(), "product": "Product Alpha"},
            {"date": (dt.date.today() + dt.timedelta(days=20)).isoformat(), "product": "Product Beta"},
        ],
        "promotions": [
            {
                "start_date": (dt.date.today() + dt.timedelta(days=10)).isoformat(),
                "end_date": (dt.date.today() + dt.timedelta(days=14)).isoformat(),
                "name": "Mid-month promo",
            }
        ],
        "evergreen_topics": [
            "How it works",
            "Feature spotlight",
            "Customer story",
            "Use-case tips",
        ],
    }
    path.write_text(json.dumps(template, indent=2))


def launch_phase(day: dt.date, launch: Launch) -> Optional[str]:
    delta = (day - launch.date).days
    if delta == -3 or delta == -2:
        return "launch_teaser"
    if delta == -1:
        return "launch_countdown"
    if delta == 0:
        return "launch_day"
    if 1 <= delta <= 3:
        return "launch_followup"
    return None


def promo_phase(day: dt.date, promo: Promotion) -> Optional[str]:
    if day < promo.start_date or day > promo.end_date:
        return None
    if day == promo.start_date:
        return "promo_start"
    if day == promo.end_date:
        return "promo_end"
    return "promo_mid"


def choose_format(platform: str, content_type: str, day_index: int) -> str:
    options = FORMAT_ROTATION[platform][content_type]
    return options[day_index % len(options)]


def generate_calendar(config: Config) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    evergreen_index = 0
    launches = sorted(config.launches, key=lambda item: item.date)
    promotions = sorted(config.promotions, key=lambda item: item.start_date)

    for offset in range(30):
        day = config.start_date + dt.timedelta(days=offset)
        content_type = "evergreen"
        phase_key = "evergreen"
        theme = config.evergreen_topics[evergreen_index % len(config.evergreen_topics)]

        for launch in launches:
            phase = launch_phase(day, launch)
            if phase:
                content_type = "launch"
                phase_key = phase
                theme = f"{launch.product} — {ANGLE_BY_PHASE[phase]}"
                break

        if content_type == "evergreen":
            for promo in promotions:
                phase = promo_phase(day, promo)
                if phase:
                    content_type = "promo"
                    phase_key = phase
                    theme = f"{promo.name} — {ANGLE_BY_PHASE[phase]}"
                    break

        if content_type == "evergreen":
            evergreen_index += 1

        for platform in PLATFORMS:
            rows.append(
                {
                    "Date": day.isoformat(),
                    "Day": day.strftime("%a"),
                    "Platform": platform,
                    "Content_Type": content_type.title(),
                    "Phase": ANGLE_BY_PHASE[phase_key],
                    "Theme": theme,
                    "Format": choose_format(platform, content_type, offset),
                    "CTA": CTA_BY_TYPE[content_type],
                    "Cadence": "1x/day",
                    "Asset": "Existing brand assets",
                }
            )

    return rows


def write_csv(rows: List[Dict[str, str]], output_path: Path) -> None:
    fieldnames = [
        "Date",
        "Day",
        "Platform",
        "Content_Type",
        "Phase",
        "Theme",
        "Format",
        "CTA",
        "Cadence",
        "Asset",
    ]
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a 30-day posting calendar CSV.")
    parser.add_argument("--config", type=Path, help="Path to a JSON config file.")
    parser.add_argument("--output", type=Path, default=Path("content_calendar.csv"), help="CSV output path.")
    parser.add_argument("--init-config", type=Path, help="Write a starter config JSON to this path.")
    args = parser.parse_args()

    if args.init_config:
        write_template(args.init_config)
        print(f"Template config written to {args.init_config}")
        return

    if not args.config:
        raise SystemExit("--config is required unless --init-config is used.")

    config = load_config(args.config)
    rows = generate_calendar(config)
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
