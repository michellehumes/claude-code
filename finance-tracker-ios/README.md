# Finance Tracker - iOS App

A native iOS finance tracking app built with SwiftUI, based on the Excel Life Tracker finance module.

<p align="center">
  <img src="https://img.shields.io/badge/iOS-15.0+-blue.svg" alt="iOS 15.0+">
  <img src="https://img.shields.io/badge/Swift-5.5+-orange.svg" alt="Swift 5.5+">
  <img src="https://img.shields.io/badge/SwiftUI-3.0+-green.svg" alt="SwiftUI 3.0+">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT License">
</p>

## Overview

Finance Tracker is a beautifully designed, privacy-first personal finance app for iPhone. Track your income and expenses, visualize spending patterns, and gain insights into your financial health — all stored locally on your device.

### Key Features

✅ **Transaction Management**
- Add, edit, and delete transactions
- Categorize by 15 built-in categories
- Track income and expenses separately
- Add notes and account information

📊 **Visual Insights**
- Monthly income vs expenses comparison
- Spending breakdown by category
- Real-time financial summaries
- Progress bars and visual indicators

🎯 **Smart Filtering**
- Filter by month, category, and type
- Search transactions by description
- Sort and organize your data
- Quick access to recent transactions

🔒 **Privacy-First**
- All data stored locally on device
- No cloud sync or account required
- No ads or tracking
- Complete data control

## Screenshots

### Dashboard
The main dashboard provides an at-a-glance view of your monthly finances:
- Total income and expenses
- Net cash flow
- Recent transactions
- Top spending categories

### Transactions
Browse all your transactions with powerful filtering:
- Filter by type (income/expense)
- Filter by category
- Navigate by month
- Swipe to delete

### Insights
Visualize your spending patterns:
- Category breakdown with percentages
- Income vs expenses comparison
- Monthly trends

### Add Transaction
Clean, simple form for adding transactions:
- Quick type selection (income/expense)
- Category picker with icons
- Date picker
- Account and owner fields
- Optional notes

## Technical Architecture

### Technology Stack
- **Language**: Swift 5.5+
- **UI Framework**: SwiftUI 3.0+
- **Minimum iOS**: 15.0
- **Data Persistence**: UserDefaults (JSON encoding)
- **Architecture**: MVVM (Model-View-ViewModel)

### Project Structure

```
FinanceTracker/
├── Models/
│   └── Transaction.swift          # Data models and enums
├── ViewModels/
│   └── FinanceDataManager.swift   # Business logic and data management
├── Views/
│   ├── ContentView.swift          # Main tab navigation
│   ├── DashboardView.swift        # Monthly summary dashboard
│   ├── TransactionsListView.swift # Transaction list with filters
│   ├── AddTransactionView.swift   # Add/edit transaction form
│   ├── TransactionDetailView.swift # Single transaction detail
│   ├── ChartsView.swift           # Visual insights and charts
│   └── SettingsView.swift         # Settings and data management
├── Utilities/
│   └── Formatters.swift           # Currency and date formatters
├── FinanceTrackerApp.swift        # App entry point
└── Info.plist                     # App configuration
```

### Data Models

**Transaction**
```swift
struct Transaction: Identifiable, Codable {
    var id: UUID
    var date: Date
    var description: String
    var category: TransactionCategory
    var type: TransactionType
    var amount: Double
    var account: String
    var owner: String
    var notes: String
}
```

**TransactionType**
- Income
- Expense

**TransactionCategory** (15 categories)
- Housing, Utilities, Groceries, Dining
- Transportation, Health, Fitness, Subscriptions
- Shopping, Travel, Education, Business
- Savings, Salary, Other

Each category has an associated SF Symbol icon for visual consistency.

## Getting Started

### Requirements
- Xcode 13.0 or later
- iOS 15.0 or later
- Swift 5.5 or later

### Installation

1. **Clone the repository**
   ```bash
   cd finance-tracker-ios
   ```

2. **Open in Xcode**
   - Open `FinanceTracker` folder in Xcode
   - Or create a new Xcode project and import these files

3. **Build and Run**
   - Select a simulator or connected device
   - Press ⌘R to build and run

### Creating an Xcode Project

If you don't have an existing Xcode project:

1. Open Xcode
2. Create New Project → iOS → App
3. Product Name: `FinanceTracker`
4. Interface: SwiftUI
5. Life Cycle: SwiftUI App
6. Language: Swift
7. Copy all files from this repository into your project
8. Maintain the folder structure shown above

## Usage Guide

### Adding Your First Transaction

1. Tap the **+** button in the navigation bar
2. Select transaction type (Income or Expense)
3. Enter description (e.g., "Grocery Shopping")
4. Choose a category
5. Enter the amount
6. Select the date
7. Optionally add account and notes
8. Tap **Add**

### Viewing Monthly Summaries

1. Navigate to the **Dashboard** tab
2. Use the left/right arrows to change months
3. View summary cards for income, expenses, and cash flow
4. See recent transactions and top categories

### Filtering Transactions

1. Go to the **Transactions** tab
2. Tap the **Type** or **Category** filter buttons
3. Select your filter criteria
4. Tap **Clear** to remove filters

### Viewing Insights

1. Navigate to the **Insights** tab
2. Select a month to analyze
3. View spending breakdown by category
4. Compare income vs expenses

### Managing Data

1. Go to **Settings** tab
2. Options:
   - **Reset to Sample Data**: Restore demo transactions
   - **Export Data**: Export transactions as JSON
   - **Clear All Data**: Delete all transactions

## Data Persistence

### Storage Method
Transactions are stored using `UserDefaults` with JSON encoding:
- Automatic save on every change
- Data persists across app launches
- No external dependencies

### Data Format
```json
[
  {
    "id": "UUID-STRING",
    "date": "2026-02-10T12:00:00Z",
    "description": "Grocery Shopping",
    "category": "groceries",
    "type": "expense",
    "amount": 85.50,
    "account": "Chase Credit",
    "owner": "Michelle",
    "notes": "Weekly shopping"
  }
]
```

### Export/Import
- **Export**: Settings → Export Data (prints JSON to console)
- **Import**: Can be extended to support file import

## Customization

### Adding New Categories

1. Open `Models/Transaction.swift`
2. Add new case to `TransactionCategory` enum
3. Add corresponding SF Symbol in `icon` computed property
4. Rebuild app

Example:
```swift
enum TransactionCategory: String, Codable, CaseIterable {
    // ... existing categories
    case entertainment = "Entertainment"

    var icon: String {
        switch self {
        // ... existing icons
        case .entertainment: return "tv.fill"
        }
    }
}
```

### Changing Currency

1. Open `Utilities/Formatters.swift`
2. Modify `currencyCode` in formatters
3. Change from "USD" to your preferred currency code

```swift
formatter.currencyCode = "EUR"  // or "GBP", "JPY", etc.
```

### Theming

All colors use system colors for automatic Dark Mode support:
- `.primary`, `.secondary` for text
- `.systemGray6` for backgrounds
- `.blue`, `.green`, `.red` for accents

To customize:
- Replace system colors with custom `Color(red:green:blue:)`
- Add color constants to a new `Theme.swift` file

## Features Roadmap

### Planned Features
- [ ] iCloud sync across devices
- [ ] Widget support for quick summary
- [ ] Recurring transactions
- [ ] Budget setting and tracking
- [ ] PDF/CSV export
- [ ] Receipt photo attachment
- [ ] Multiple accounts support
- [ ] Custom categories
- [ ] Reports and analytics
- [ ] Search functionality
- [ ] Biometric lock
- [ ] Multi-currency support

### Future Enhancements
- [ ] Charts using Swift Charts framework (iOS 16+)
- [ ] Siri shortcuts integration
- [ ] Apple Watch companion app
- [ ] SharePlay for shared expenses
- [ ] Tags and custom fields
- [ ] Advanced filtering and sorting

## Performance

### Optimization
- Lazy loading of transaction lists
- Efficient filtering with Swift's native methods
- Minimal re-renders with SwiftUI state management
- JSON encoding for compact storage

### Scalability
- Tested with 1000+ transactions
- Smooth scrolling and filtering
- Instant summary calculations
- Responsive UI updates

## Privacy & Security

### Data Privacy
- ✅ All data stored locally
- ✅ No network requests
- ✅ No analytics or tracking
- ✅ No user accounts required
- ✅ Complete data ownership

### Recommended Security
- Enable device passcode
- Use Face ID/Touch ID
- Regular backups via iCloud device backup
- Export data periodically

## Troubleshooting

### Common Issues

**App crashes on launch**
- Solution: Delete app and reinstall
- Your data is stored in UserDefaults and will persist

**Transactions not saving**
- Check storage space on device
- Restart the app
- Try resetting to sample data

**Filters not working**
- Ensure transactions exist for selected month
- Clear filters and reapply
- Check selected filter values

## Contributing

This app was built for personal use but can be extended:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow Swift API Design Guidelines
- Use SwiftLint for consistent formatting
- Comment complex logic
- Write descriptive commit messages

## Credits

**Built for**: Michelle (Shelzy) Humes
**Based on**: Excel Life Tracker finance module
**Framework**: SwiftUI
**Icons**: SF Symbols
**Date**: February 2026

## License

MIT License - feel free to use and modify for personal or commercial use.

## Support

For questions or issues:
- Create an issue on GitHub
- Check the Excel Life Tracker documentation
- Review SwiftUI documentation at [developer.apple.com](https://developer.apple.com/documentation/swiftui/)

## Acknowledgments

- Apple SwiftUI team for the amazing framework
- SF Symbols for beautiful, consistent icons
- The Excel Life Tracker project for inspiration

---

**Made with ❤️ and SwiftUI**
