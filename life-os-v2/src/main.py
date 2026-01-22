#!/usr/bin/env python3
"""
Life OS v2 - Complete 54-Tab Life Management System

Main entry point for creating and populating the Google Sheets system.

Usage:
    # Create a new spreadsheet
    python src/main.py --create "Life OS v2"

    # Update an existing spreadsheet
    python src/main.py --spreadsheet-id YOUR_SPREADSHEET_ID

    # Export to Excel (offline mode)
    python src/main.py --export-excel

    # Export to CSV (offline mode)
    python src/main.py --export-csv
"""

import argparse
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.spreadsheet_builder import SpreadsheetBuilder, OfflineSpreadsheetBuilder
from src.data_processors.transactions import TransactionProcessor
from src.data_processors.oura import OuraDataProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Life OS v2 - 54-Tab Google Sheets Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --create "Life OS v2"
  python src/main.py --spreadsheet-id abc123xyz
  python src/main.py --export-excel
  python src/main.py --export-csv

Data Files:
  Place your data files in the data/ directory:
  - data/transactions.csv (Monarch Money export)
  - data/oura/ (Oura Ring exports)
        """
    )

    parser.add_argument(
        "--create",
        metavar="TITLE",
        help="Create a new spreadsheet with the given title"
    )

    parser.add_argument(
        "--spreadsheet-id",
        metavar="ID",
        help="Update an existing spreadsheet by ID"
    )

    parser.add_argument(
        "--credentials",
        metavar="PATH",
        default="config/credentials.json",
        help="Path to Google API credentials JSON file"
    )

    parser.add_argument(
        "--transactions",
        metavar="PATH",
        help="Path to Monarch Money transactions CSV"
    )

    parser.add_argument(
        "--oura-dir",
        metavar="PATH",
        help="Path to directory containing Oura data exports"
    )

    parser.add_argument(
        "--export-excel",
        action="store_true",
        help="Export to Excel file (offline mode, no Google API needed)"
    )

    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Export to CSV files (offline mode, no Google API needed)"
    )

    parser.add_argument(
        "--output",
        metavar="PATH",
        default="data/export",
        help="Output directory/file for exports"
    )

    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Use sample data instead of importing from files"
    )

    args = parser.parse_args()

    # Header
    print("=" * 60)
    print("  LIFE OS v2 - 54-Tab Life Management System")
    print("  For Michelle & Gray Perkins")
    print("=" * 60)
    print()

    # Load data if paths provided
    transaction_data = None
    oura_data = None

    if args.transactions and os.path.exists(args.transactions):
        print(f"Loading transactions from {args.transactions}...")
        try:
            processor = TransactionProcessor(args.transactions)
            processor.load_csv()
            transaction_data = processor.get_transactions_data()
            print(f"  ✓ Loaded {len(transaction_data)} transactions")
        except Exception as e:
            print(f"  ✗ Failed to load transactions: {e}")

    if args.oura_dir and os.path.isdir(args.oura_dir):
        print(f"Loading Oura data from {args.oura_dir}...")
        try:
            oura_processor = OuraDataProcessor(args.oura_dir)
            files = oura_processor.load_all_data()
            oura_data = oura_processor
            print(f"  ✓ Loaded Oura data: {', '.join(files)}")
        except Exception as e:
            print(f"  ✗ Failed to load Oura data: {e}")

    if args.sample_data:
        print("Using sample data...")
        transaction_data = TransactionProcessor.generate_sample_data()
        print(f"  ✓ Generated {len(transaction_data)} sample transactions")

    # Determine mode
    if args.export_excel or args.export_csv:
        # Offline mode
        print("\nRunning in offline mode (no Google API)...")
        builder = OfflineSpreadsheetBuilder()
        builder.build_all_tabs(transaction_data, oura_data)

        if args.export_excel:
            output_path = args.output if args.output.endswith('.xlsx') else os.path.join(args.output, "LifeOS_v2.xlsx")
            builder.export_to_excel(output_path)

        if args.export_csv:
            builder.export_to_csv(args.output)

    elif args.create or args.spreadsheet_id:
        # Online mode - requires Google API
        builder = SpreadsheetBuilder(args.credentials)

        if not builder.authenticate():
            print("\nAuthentication failed. Please check your credentials file.")
            print("See README.md for setup instructions.")
            sys.exit(1)

        if args.create:
            spreadsheet_id = builder.create_spreadsheet(args.create)
            if not spreadsheet_id:
                print("Failed to create spreadsheet.")
                sys.exit(1)
        else:
            if not builder.open_spreadsheet(args.spreadsheet_id):
                print("Failed to open spreadsheet.")
                sys.exit(1)

        # Build all tabs
        results = builder.build_all_tabs(transaction_data, oura_data)

        # Summary
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)

        print()
        print("=" * 60)
        print(f"  BUILD COMPLETE: {success_count}/{total_count} tabs successful")
        print("=" * 60)
        print()
        print(f"Spreadsheet URL: {builder.get_spreadsheet_url()}")

    else:
        # No mode specified, show help
        parser.print_help()
        print()
        print("Quick Start:")
        print("  1. Set up Google API credentials (see README.md)")
        print("  2. Run: python src/main.py --create 'Life OS v2'")
        print()
        print("Or for offline mode (no Google API needed):")
        print("  python src/main.py --export-excel --sample-data")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
