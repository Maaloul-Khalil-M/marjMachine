const fs = require('fs');
const path = require('path');

// Read config file
const configPath = path.join(__dirname, 'time_periods.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const now = new Date();
const hour = now.getHours();
const minute = now.getMinutes();

// Find current period
let currentPeriod = null;
for (const period of config.periods) {
  const { start, end } = period;
  
  // Handle periods that cross midnight (e.g., 19 -> 1)
  if (start > end) {
    if (hour >= start || hour < end) {
      currentPeriod = period;
      break;
    }
  } else {
    if (hour >= start && hour < end) {
      currentPeriod = period;
      break;
    }
  }
}

if (!currentPeriod) {
  console.log(JSON.stringify({ icon: "⏰", error: "No period found" }));
  process.exit(1);
}

// Calculate end time
const end = new Date(now);
if (currentPeriod.start > currentPeriod.end && hour >= currentPeriod.start) {
  // Period crosses midnight and we're before midnight
  end.setDate(end.getDate() + 1);
}
end.setHours(currentPeriod.end, 0, 0, 0);

// Calculate remaining time
const diff = Math.max(0, end - now);
const totalMinutes = Math.floor(diff / 60000);
const h = Math.floor(totalMinutes / 60);
const m = totalMinutes % 60;

// Calculate total period duration and progress
const periodStart = new Date(now);
if (currentPeriod.start > currentPeriod.end && hour < currentPeriod.end) {
  // We're past midnight in a period that started yesterday
  periodStart.setDate(periodStart.getDate() - 1);
}
periodStart.setHours(currentPeriod.start, 0, 0, 0);

const totalDuration = end - periodStart;
const elapsed = now - periodStart;
const progress = Math.round((elapsed / totalDuration) * 100);

// Find next period
const currentIndex = config.periods.indexOf(currentPeriod);
const nextPeriod = config.periods[(currentIndex + 1) % config.periods.length];

// Create progress bar (8 blocks)
const blocks = 8;
const filled = Math.round((progress / 100) * blocks);
const progressBar = '█'.repeat(filled) + '░'.repeat(blocks - filled);

console.log(JSON.stringify({
  icon: currentPeriod.icon,
  name: currentPeriod.name,
  description: currentPeriod.description,
  remaining: `${h}h ${m}m`,
  progress: progress,
  progressBar: progressBar,
  nextIcon: nextPeriod.icon,
  nextName: nextPeriod.name,
  timeUntilNext: `${h}h ${m}m`
}));