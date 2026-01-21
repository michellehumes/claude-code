#!/usr/bin/env node

/**
 * Freelance Job Monitor
 *
 * This script helps you monitor freelance platforms for urgent opportunities.
 * It provides a notification system and job tracking.
 *
 * Usage: node job-monitor.js
 */

const https = require('https');
const { exec } = require('child_process');

// Configuration
const CONFIG = {
  checkInterval: 5 * 60 * 1000, // Check every 5 minutes
  urgentKeywords: ['urgent', 'asap', 'today', 'rush', 'immediate', 'emergency', 'express', 'quick'],
  minBudget: 50,
  notificationSound: true,
};

// Job storage
let previousJobs = new Set();
let sessionStats = {
  startTime: new Date(),
  jobsFound: 0,
  applicationsRecommended: 0,
  lastCheck: null,
};

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

/**
 * Print colored output
 */
function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Print banner
 */
function printBanner() {
  console.clear();
  log('═══════════════════════════════════════════════════', 'cyan');
  log('    💰 QUICK MONEY JOB MONITOR 💰', 'bright');
  log('    Hunting for $100 in 2 hours!', 'yellow');
  log('═══════════════════════════════════════════════════', 'cyan');
  console.log();
}

/**
 * Play notification sound (cross-platform)
 */
function playNotification() {
  if (!CONFIG.notificationSound) return;

  // Try to play system sound
  const commands = {
    darwin: 'afplay /System/Library/Sounds/Glass.aiff',
    linux: 'paplay /usr/share/sounds/freedesktop/stereo/message.oga || beep',
    win32: 'powershell -c (New-Object Media.SoundPlayer "C:\\Windows\\Media\\notify.wav").PlaySync()',
  };

  const command = commands[process.platform];
  if (command) {
    exec(command, () => {});
  }
}

/**
 * Send desktop notification (cross-platform)
 */
function sendDesktopNotification(title, message) {
  const commands = {
    darwin: `osascript -e 'display notification "${message}" with title "${title}"'`,
    linux: `notify-send "${title}" "${message}"`,
    win32: `powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('${message}', '${title}')}"`,
  };

  const command = commands[process.platform];
  if (command) {
    exec(command, () => {});
  }
}

/**
 * Check if job description contains urgent keywords
 */
function isUrgent(text) {
  const lowerText = text.toLowerCase();
  return CONFIG.urgentKeywords.some(keyword => lowerText.includes(keyword));
}

/**
 * Extract budget from job description
 */
function extractBudget(text) {
  const patterns = [
    /\$(\d+)/,
    /(\d+)\s*USD/i,
    /budget:\s*\$?(\d+)/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return parseInt(match[1]);
    }
  }

  return null;
}

/**
 * Print session statistics
 */
function printStats() {
  const runtime = Math.floor((new Date() - sessionStats.startTime) / 1000 / 60);
  log('\n📊 SESSION STATS', 'cyan');
  log('─────────────────────────────────────────', 'cyan');
  log(`Runtime: ${runtime} minutes`, 'white');
  log(`Jobs Found: ${sessionStats.jobsFound}`, 'white');
  log(`Applications Recommended: ${sessionStats.applicationsRecommended}`, 'white');
  log(`Last Check: ${sessionStats.lastCheck || 'Never'}`, 'white');
  log('─────────────────────────────────────────\n', 'cyan');
}

/**
 * Manual job entry - allows you to track jobs you find manually
 */
function promptForManualEntry() {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  log('\n📝 MANUAL JOB TRACKING', 'yellow');
  log('Found a job manually? Enter details (or press Enter to skip):\n', 'white');

  readline.question('Job Title: ', (title) => {
    if (!title) {
      readline.close();
      return;
    }

    readline.question('Platform (Upwork/Fiverr/Other): ', (platform) => {
      readline.question('Budget ($): ', (budget) => {
        readline.question('Is it urgent? (y/n): ', (urgent) => {
          const job = {
            title,
            platform: platform || 'Unknown',
            budget: budget ? `$${budget}` : 'Not specified',
            urgent: urgent.toLowerCase() === 'y',
            addedAt: new Date().toLocaleTimeString(),
          };

          log('\n✅ Job tracked!', 'green');
          displayJob(job, true);

          sessionStats.jobsFound++;
          if (job.urgent || parseInt(budget) >= CONFIG.minBudget) {
            sessionStats.applicationsRecommended++;
          }

          readline.close();
        });
      });
    });
  });
}

/**
 * Display a job opportunity
 */
function displayJob(job, isNew = false) {
  const prefix = isNew ? '🔥 NEW URGENT JOB' : '📌 JOB';
  const color = isNew ? 'green' : 'yellow';

  log(`\n${prefix}`, color);
  log('─────────────────────────────────────────', color);
  log(`Title: ${job.title}`, 'bright');
  if (job.platform) log(`Platform: ${job.platform}`, 'white');
  if (job.budget) log(`Budget: ${job.budget}`, 'white');
  if (job.urgent) log(`⚡ URGENT - Apply immediately!`, 'red');
  if (job.addedAt) log(`Found at: ${job.addedAt}`, 'white');
  log('─────────────────────────────────────────\n', color);

  if (isNew) {
    playNotification();
    sendDesktopNotification('New Urgent Job!', job.title);
  }
}

/**
 * Provide search suggestions
 */
function printSearchSuggestions() {
  log('\n🔍 RECOMMENDED SEARCH TERMS FOR UPWORK:', 'magenta');
  log('─────────────────────────────────────────', 'magenta');

  const suggestions = [
    'urgent website bug fix',
    'ASAP logo design',
    'quick blog article needed',
    'rush JavaScript help',
    'today content writing',
    'immediate WordPress fix',
    'express graphic design',
    'same day article writing',
  ];

  suggestions.forEach((term, idx) => {
    log(`${idx + 1}. "${term}"`, 'white');
  });

  log('─────────────────────────────────────────\n', 'magenta');
}

/**
 * Print action items
 */
function printActionItems() {
  log('⚡ IMMEDIATE ACTIONS:', 'yellow');
  log('─────────────────────────────────────────', 'yellow');
  log('1. Open Upwork and search for urgent jobs', 'white');
  log('2. Check Fiverr Buyer Requests', 'white');
  log('3. Set your status to "Available Now"', 'white');
  log('4. Apply to 5-10 jobs in the next 15 minutes', 'white');
  log('5. Use proposal templates from proposal-templates.md', 'white');
  log('─────────────────────────────────────────\n', 'yellow');
}

/**
 * Timer reminder
 */
function startTimerReminders() {
  const intervals = [15, 30, 45, 60, 90, 120]; // minutes

  intervals.forEach(minutes => {
    setTimeout(() => {
      log(`\n⏰ ${minutes} MINUTE MARK!`, 'red');

      if (minutes === 15) {
        log('Check: Have you applied to 10+ jobs?', 'yellow');
      } else if (minutes === 30) {
        log('Check: Any responses yet? Keep applying!', 'yellow');
      } else if (minutes === 60) {
        log('Halfway point! Status check:', 'yellow');
        log('- Applied to 20+ jobs?', 'white');
        log('- Any client conversations?', 'white');
        log('- Still checking platforms every 15 min?', 'white');
      } else if (minutes === 90) {
        log('30 minutes left! Final push:', 'yellow');
        log('- Send 10 more proposals', 'white');
        log('- Lower prices if needed', 'white');
        log('- Check all messages', 'white');
      } else if (minutes === 120) {
        log('🎯 2 HOUR MARK REACHED!', 'yellow');
        log('Time to review results and plan next steps', 'white');
        printFinalReport();
      }

      playNotification();
      sendDesktopNotification(`${minutes} Minute Mark!`, 'Time for a status check');
    }, minutes * 60 * 1000);
  });
}

/**
 * Print final report
 */
function printFinalReport() {
  printStats();

  log('📋 FINAL CHECKLIST:', 'cyan');
  log('─────────────────────────────────────────', 'cyan');
  log('□ Did you land a job?', 'white');
  log('□ Did you apply to 25+ positions?', 'white');
  log('□ Are your gigs optimized and live?', 'white');
  log('□ Did you respond to all messages?', 'white');
  log('─────────────────────────────────────────\n', 'cyan');

  log('💡 NEXT STEPS:', 'green');
  log('─────────────────────────────────────────', 'green');
  log('If you earned $100: Celebrate! 🎉', 'white');
  log('If you earned $50-99: Great progress! Finish delivery.', 'white');
  log('If no jobs yet: Your proposals are still active!', 'white');
  log('  → Check again tomorrow morning', 'white');
  log('  → Responses often come 12-48 hours later', 'white');
  log('  → Keep profiles active and online', 'white');
  log('─────────────────────────────────────────\n', 'green');
}

/**
 * Interactive menu
 */
function showMenu() {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  log('\n📋 MENU:', 'cyan');
  log('1. Track a job manually', 'white');
  log('2. View search suggestions', 'white');
  log('3. View action items', 'white');
  log('4. View session stats', 'white');
  log('5. Exit', 'white');
  console.log();

  readline.question('Select option (1-5): ', (answer) => {
    readline.close();

    switch(answer.trim()) {
      case '1':
        promptForManualEntry();
        setTimeout(showMenu, 2000);
        break;
      case '2':
        printSearchSuggestions();
        setTimeout(showMenu, 1000);
        break;
      case '3':
        printActionItems();
        setTimeout(showMenu, 1000);
        break;
      case '4':
        printStats();
        setTimeout(showMenu, 1000);
        break;
      case '5':
        log('\n👋 Good luck! You got this! 💪\n', 'green');
        process.exit(0);
        break;
      default:
        log('Invalid option', 'red');
        setTimeout(showMenu, 1000);
    }
  });
}

/**
 * Main function
 */
function main() {
  printBanner();

  log('🚀 STARTING 2-HOUR MONEY SPRINT!\n', 'green');
  log('This tool will help you track your progress and remind you to check platforms.\n', 'white');

  printActionItems();
  printSearchSuggestions();

  // Start timer reminders
  startTimerReminders();
  log('⏰ Timer reminders set for 15, 30, 45, 60, 90, and 120 minutes\n', 'cyan');

  // Show menu
  setTimeout(showMenu, 2000);
}

// Run the script
main();
