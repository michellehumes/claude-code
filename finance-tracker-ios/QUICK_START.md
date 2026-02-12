# Finance Tracker - Quick Start Guide

Get up and running with the Finance Tracker iOS app in minutes.

## 📱 Opening in Xcode

### Option 1: Create New Xcode Project (Recommended)

1. **Open Xcode**

2. **Create New Project**
   - File → New → Project (⇧⌘N)
   - Choose **iOS → App**
   - Click **Next**

3. **Configure Project**
   - **Product Name**: `FinanceTracker`
   - **Team**: Your development team (or None for simulator only)
   - **Organization Identifier**: `com.yourname` (or any identifier)
   - **Interface**: **SwiftUI**
   - **Life Cycle**: **SwiftUI App**
   - **Language**: **Swift**
   - **Use Core Data**: ❌ Unchecked
   - **Include Tests**: ✅ Optional
   - Click **Next**

4. **Choose Location**
   - Save anywhere convenient
   - Click **Create**

5. **Import Source Files**
   - Delete the default `ContentView.swift` file Xcode created
   - In Finder, open the `finance-tracker-ios/FinanceTracker/` folder
   - Drag all files and folders into your Xcode project:
     - `Models/` folder
     - `Views/` folder
     - `ViewModels/` folder
     - `Utilities/` folder
     - `FinanceTrackerApp.swift`
     - `Info.plist`
   - When prompted:
     - ✅ Check "Copy items if needed"
     - ✅ Select "Create groups"
     - ✅ Add to target: FinanceTracker

6. **Build and Run**
   - Select a simulator (iPhone 14 Pro recommended)
   - Press **⌘R** or click the Play button
   - App should launch with sample data

### Option 2: Use Existing Project Structure

If you want to use the files directly:

1. Open Xcode
2. File → Open
3. Navigate to `finance-tracker-ios/`
4. Select the folder
5. You'll need to create a project manually or use `swift package init`

## 🎯 First Launch

When you first launch the app:

1. **Explore Sample Data**
   - The app includes 8 sample transactions
   - Navigate through tabs: Dashboard, Transactions, Insights, Settings

2. **Try Adding a Transaction**
   - Tap the **+** button in the top right
   - Fill in the form:
     - Type: Expense
     - Description: "Coffee"
     - Category: Dining
     - Amount: 5.00
   - Tap **Add**

3. **View Your Dashboard**
   - Go to Dashboard tab
   - See updated totals and recent transactions

4. **Explore Insights**
   - Go to Insights tab
   - View spending breakdown by category
   - See income vs expenses comparison

## 🔧 Xcode Configuration

### Build Settings
No special configuration needed! The app uses:
- Standard Swift compilation
- SwiftUI framework (built-in)
- No external dependencies
- No CocoaPods or SPM packages

### Deployment Target
- Minimum: iOS 15.0
- Recommended: iOS 16.0+ for best performance

### Capabilities
No special capabilities required:
- ❌ No network access
- ❌ No location services
- ❌ No camera/photos
- ✅ Just UserDefaults for storage

## 📂 Project Structure in Xcode

After importing, your project should look like:

```
FinanceTracker/
├── 📁 Models/
│   └── Transaction.swift
├── 📁 ViewModels/
│   └── FinanceDataManager.swift
├── 📁 Views/
│   ├── ContentView.swift
│   ├── DashboardView.swift
│   ├── TransactionsListView.swift
│   ├── AddTransactionView.swift
│   ├── TransactionDetailView.swift
│   ├── ChartsView.swift
│   └── SettingsView.swift
├── 📁 Utilities/
│   └── Formatters.swift
├── FinanceTrackerApp.swift
└── Info.plist
```

## 🏃‍♂️ Running on Device

### Prerequisites
1. Apple Developer Account (free or paid)
2. iPhone with iOS 15.0+
3. USB cable

### Steps
1. Connect iPhone via USB
2. In Xcode, select your iPhone from the device dropdown
3. Go to **Signing & Capabilities** tab
4. Select your Team
5. Click **⌘R** to build and run
6. On iPhone: **Settings → General → VPN & Device Management**
7. Trust your developer certificate
8. Launch app

## 🧪 Testing

### Simulator Testing
- **iPhone 14 Pro**: Best for testing (recommended)
- **iPhone SE**: Test small screen layout
- **iPad**: Test on larger screens

### Feature Checklist
- [ ] Add a transaction
- [ ] Edit a transaction
- [ ] Delete a transaction
- [ ] Filter by category
- [ ] Filter by type
- [ ] Navigate between months
- [ ] View insights/charts
- [ ] Reset to sample data
- [ ] Clear all data

## 🐛 Common Issues

### "No such module 'SwiftUI'"
- **Solution**: Ensure deployment target is iOS 15.0+
- Check Xcode version is 13.0 or later

### "Cannot find 'FinanceDataManager' in scope"
- **Solution**: Make sure all files are added to your target
- Project Navigator → Select file → Target Membership → Check FinanceTracker

### App crashes on launch
- **Solution**: Check Console for error messages
- Common: Missing files or incorrect imports

### Preview not working
- **Solution**: Clean build folder (⇧⌘K)
- Rebuild (⌘B)
- Try different preview

## 💡 Quick Tips

### Keyboard Shortcuts
- **⌘R**: Build and Run
- **⌘B**: Build
- **⌘.**: Stop running app
- **⌥⌘P**: Resume SwiftUI preview
- **⇧⌘K**: Clean build folder

### Development Workflow
1. Make changes in code
2. Use SwiftUI previews for instant feedback
3. Run in simulator to test full flow
4. Test on device before release

### Debugging
- Use `print()` statements in code
- Check Xcode console for output
- Use breakpoints for complex debugging
- SwiftUI preview for visual debugging

## 📊 Sample Data

The app includes realistic sample data:
- 2 income transactions (salary, business income)
- 6 expense transactions (rent, groceries, bills, shopping)
- Spread across the last 10 days
- Total income: $4,950
- Total expenses: ~$2,200

### Resetting Data
1. Go to **Settings** tab
2. Tap **Reset to Sample Data**
3. Confirm the action

### Starting Fresh
1. Go to **Settings** tab
2. Tap **Clear All Data**
3. Confirm the action
4. Start adding your own transactions

## 🚀 Next Steps

1. **Customize Categories**
   - Edit `Models/Transaction.swift`
   - Add your own categories and icons

2. **Change Currency**
   - Edit `Utilities/Formatters.swift`
   - Update `currencyCode` property

3. **Add Features**
   - Implement recurring transactions
   - Add budget tracking
   - Create reports

4. **Enhance UI**
   - Customize colors and styling
   - Add animations
   - Improve layouts

## 📚 Learning Resources

- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui) - Official Apple tutorials
- [Swift Documentation](https://docs.swift.org) - Swift language guide
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) - iOS design principles

## 🎉 You're Ready!

The app is now running. Explore the features, add your own data, and customize it to fit your needs!

---

**Need help?** Check the main README.md for detailed documentation.
