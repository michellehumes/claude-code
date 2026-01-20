/***************
 LIFE OS AUTOMATION ENGINE

 Setup Instructions:
 1. Upload LIFE_Master_Tracker_AUTOMATION_READY.xlsx to Google Drive
 2. Right-click → Open with → Google Sheets (converts to native Sheet)
 3. Rename to "LIFE_OS_MASTER (LIVE)"
 4. Go to Extensions → Apps Script
 5. Delete starter code and paste this entire file
 6. Save (Ctrl+S) and authorize permissions when prompted
 7. Set up triggers via Triggers icon (clock) in left sidebar
***************/

function weeklyExecSummaryEmail() {
  const ss = SpreadsheetApp.getActive();
  const summary = ss.getSheetByName("🧾 Weekly Exec Summary");
  const range = summary.getRange("A3:B20").getDisplayValues();

  let body = "Weekly Executive Summary\n\n";
  range.forEach(r => {
    if (r[0]) body += `${r[0]}: ${r[1]}\n`;
  });

  MailApp.sendEmail({
    to: Session.getActiveUser().getEmail(),
    subject: "📊 Weekly Life OS Executive Summary",
    body: body
  });
}

/***************
 JOB STALL ALERTS
***************/
function stalledInterviewAlerts() {
  const ss = SpreadsheetApp.getActive();
  const pipeline = ss.getSheetByName("📈 Job Pipeline");
  const data = pipeline.getDataRange().getValues();

  const today = new Date();
  let alerts = [];

  for (let i = 1; i < data.length; i++) {
    const [company, role,, , , lastTouch,, status] = data[i];
    if (status === "Active" && lastTouch) {
      const diff = (today - new Date(lastTouch)) / (1000 * 60 * 60 * 24);
      if (diff > 14) {
        alerts.push(`${company} – ${role} (${Math.floor(diff)} days idle)`);
      }
    }
  }

  if (alerts.length) {
    MailApp.sendEmail({
      to: Session.getActiveUser().getEmail(),
      subject: "⚠️ Stalled Job Pipeline Alerts",
      body: alerts.join("\n")
    });
  }
}

/***************
 WEEKLY RUNNER
***************/
function weeklyLifeOS() {
  weeklyExecSummaryEmail();
  stalledInterviewAlerts();
}

/***************
 JOB FEED INGESTION
***************/
function ingestJobFeed() {
  const sheet = SpreadsheetApp.getActive().getSheetByName("🔎 Job Feed (Auto)");

  const feeds = [
    "https://www.indeed.com/rss?q=VP+Healthcare+Media",
    "https://www.indeed.com/rss?q=Director+Pharma+Media"
  ];

  feeds.forEach(url => {
    try {
      const xml = UrlFetchApp.fetch(url).getContentText();
      const items = xml.match(/<item>[\s\S]*?<\/item>/g) || [];

      items.forEach(item => {
        const title = item.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/)?.[1];
        const link = item.match(/<link>(.*?)<\/link>/)?.[1];
        const company = item.match(/<source>(.*?)<\/source>/)?.[1] || "";

        if (title && !linkExists(sheet, link)) {
          sheet.appendRow([
            "Indeed",
            company,
            title,
            "",
            link,
            new Date()
          ]);
        }
      });
    } catch (e) {
      Logger.log("Error fetching feed: " + url + " - " + e.message);
    }
  });
}

function linkExists(sheet, link) {
  const links = sheet.getRange("E:E").getValues().flat();
  return links.includes(link);
}

/***************
 MANUAL TEST FUNCTIONS
 Run these to verify setup before enabling triggers
***************/
function testWeeklySummary() {
  Logger.log("Testing Weekly Executive Summary...");
  weeklyExecSummaryEmail();
  Logger.log("Email sent successfully!");
}

function testStalledAlerts() {
  Logger.log("Testing Stalled Interview Alerts...");
  stalledInterviewAlerts();
  Logger.log("Check complete!");
}

function testJobFeed() {
  Logger.log("Testing Job Feed Ingestion...");
  ingestJobFeed();
  Logger.log("Feed ingestion complete!");
}
