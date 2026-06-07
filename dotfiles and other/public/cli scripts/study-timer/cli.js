#!/usr/bin/env node
'use strict';

const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');
const { default: chalk } = require('chalk');
const { execSync } = require('child_process');

const { loadData, saveData } = require('./store');
const {
  getTodayKey,
  getDateKey,
  formatDuration,
  formatMins,
  getTodayTotal,
  getGoalPercent,
  buildSessionRecord,
  calcCurrentStreak,
  calcLongestStreak,
  groupByDate,
  groupByTopic,
  pickMotivation,
  getDataFilePath,
} = require('./helpers');

// ─── Open a URL in the default browser (cross-platform) ───────────────────

function openUrl(url) {
  try {
    const platform = process.platform;
    if (platform === 'win32') execSync(`start "" "${url}"`, { stdio: 'ignore' });
    else if (platform === 'darwin') execSync(`open "${url}"`, { stdio: 'ignore' });
    else execSync(`xdg-open "${url}"`, { stdio: 'ignore' });
  } catch {
    // Silently ignore — link opening is best-effort
  }
}

// ─── UI helpers ───────────────────────────────────────────────────────────

const line = () => console.log(chalk.dim('─'.repeat(44)));

// ─── Commands ─────────────────────────────────────────────────────────────

yargs(hideBin(process.argv))

  // START
  .command(
    'start [topic]',
    'Start a study session',
    (y) => y.positional('topic', { type: 'string', default: 'General Study' }),
    (argv) => {
      const data = loadData();

      if (data.currentSession) {
        console.log(chalk.yellow('You already have an active session.'));
        console.log(`Topic: ${chalk.bold(data.currentSession.topic)}`);
        console.log('Run ' + chalk.cyan('study stop') + ' first.');
        return;
      }

      const now = new Date().toISOString();
      data.currentSession = { startTime: now, topic: argv.topic };
      saveData(data);

      const motivation = pickMotivation();

      line();
      console.log(chalk.green('Session started'));
      console.log(`Topic    ${chalk.bold(argv.topic)}`);
      console.log(`Time     ${new Date(now).toLocaleTimeString()}`);
      console.log(`Data     ${chalk.dim(getDataFilePath())}`);
      console.log('');
      console.log(chalk.dim(motivation.text));

      if (motivation.url) {
        console.log(chalk.dim('Opening motivation link...'));
        openUrl(motivation.url);
      }
      line();
    }
  )

  // STOP
  .command(
    'stop',
    'Stop and save the current session',
    {},
    () => {
      const data = loadData();

      if (!data.currentSession) {
        console.log(chalk.yellow('No active session.'));
        console.log('Run ' + chalk.cyan('study start') + ' to begin.');
        return;
      }

      const now = new Date();
      const session = buildSessionRecord(data.currentSession, now);
      const today = getTodayKey(now);

      data.sessions.push({
        date: session.date,
        topic: session.topic,
        startTime: session.startTime,
        endTime: session.endTime,
        durationMinutes: session.durationMinutes,
      });
      data.currentSession = null;
      saveData(data);

      const todayTotal = getTodayTotal(data.sessions, today);
      const goal = data.dailyGoalMinutes || 60;
      const pct = getGoalPercent(todayTotal, goal);
      const motivation = pickMotivation();

      line();
      console.log(chalk.green('Session saved'));
      console.log(`Topic    ${chalk.bold(session.topic)}`);
      console.log(`Duration ${chalk.bold(formatDuration(session.durationMs))}`);
      console.log(`Today    ${formatMins(todayTotal)} total  (${pct}% of ${formatMins(goal)} goal)`);
      console.log('');
      console.log(chalk.dim(motivation.text));
      if (motivation.url) console.log(chalk.dim(motivation.url));
      line();
    }
  )

  // STATUS
  .command(
    'status',
    "Show current session and today's progress",
    {},
    () => {
      const data = loadData();
      const today = getTodayKey();

      line();
      if (data.currentSession) {
        const elapsed = Date.now() - new Date(data.currentSession.startTime).getTime();
        console.log(chalk.green('Active session'));
        console.log(`Topic    ${chalk.bold(data.currentSession.topic)}`);
        console.log(`Elapsed  ${chalk.bold(formatDuration(elapsed))}`);
      } else {
        console.log(chalk.dim('No active session'));
      }

      const todayTotal = getTodayTotal(data.sessions, today);
      const goal = data.dailyGoalMinutes || 60;
      const pct = getGoalPercent(todayTotal, goal);
      console.log(`Today    ${formatMins(todayTotal)} completed  (${pct}% of ${formatMins(goal)} goal)`);
      line();
    }
  )

  // REVIEW
  .command(
    'review [days]',
    'Show study history for the last N days (default 7)',
    (y) => y.positional('days', { type: 'number', default: 7 }),
    (argv) => {
      const data = loadData();
      const n = Math.max(1, Math.min(argv.days, 30));
      const goal = data.dailyGoalMinutes || 60;
      const byDate = groupByDate(data.sessions);
      const dates = Array.from({ length: n }, (_, i) => getDateKey(n - 1 - i));
      const today = getTodayKey();
      const weekTotal = dates.reduce((sum, d) => sum + (byDate[d] || 0), 0);

      line();
      console.log(chalk.bold(`Last ${n} days`));
      console.log('');

      for (const d of dates) {
        const mins = byDate[d] || 0;
        const met = mins >= goal;
        const label = d === today ? chalk.cyan(d + ' (today)') : chalk.dim(d);
        const time =
          mins > 0
            ? met
              ? chalk.green(formatMins(mins))
              : chalk.yellow(formatMins(mins))
            : chalk.dim('0m');
        const mark = met ? chalk.green(' goal met') : '';
        console.log(`  ${label}  ${time}${mark}`);
      }

      console.log('');
      console.log(`Total    ${chalk.bold(formatMins(weekTotal))}  over ${n} days`);
      console.log(`Average  ${chalk.bold(formatMins(Math.round(weekTotal / n)))} per day`);
      line();
    }
  )

  // STREAK
  .command(
    'streak',
    'Show your current and longest study streak',
    {},
    () => {
      const data = loadData();
      const goal = data.dailyGoalMinutes || 60;
      const current = calcCurrentStreak(data.sessions, goal);
      const longest = calcLongestStreak(data.sessions, goal);

      line();
      console.log(chalk.bold('Streak'));
      console.log('');
      console.log(`Current   ${chalk.bold(current)} day${current !== 1 ? 's' : ''}`);
      console.log(`Longest   ${chalk.bold(longest)} day${longest !== 1 ? 's' : ''}`);
      console.log('');

      if (current === 0) {
        console.log(chalk.dim('Study today to start a streak.'));
      } else if (current >= 30) {
        console.log(chalk.green('30 days strong. Incredible.'));
      } else if (current >= 7) {
        console.log(chalk.green('One week streak. Keep it going.'));
      } else {
        const left = 7 - current;
        console.log(chalk.dim(`${left} more day${left !== 1 ? 's' : ''} to reach a week streak.`));
      }
      line();
    }
  )

  // TOPICS
  .command(
    'topics',
    'Show time spent per topic',
    {},
    () => {
      const data = loadData();

      if (data.sessions.length === 0) {
        console.log(chalk.dim('No sessions recorded yet.'));
        return;
      }

      const byTopic = groupByTopic(data.sessions);
      const sorted = Object.entries(byTopic).sort((a, b) => b[1] - a[1]);
      const totalMins = sorted.reduce((sum, [, m]) => sum + m, 0);

      line();
      console.log(chalk.bold('Topics'));
      console.log('');

      for (const [topic, mins] of sorted) {
        const pct = Math.round((mins / totalMins) * 100);
        console.log(
          `  ${chalk.bold(topic.padEnd(20))}  ${formatMins(mins).padStart(6)}  ${chalk.dim(pct + '%')}`
        );
      }

      console.log('');
      console.log(`Total  ${chalk.bold(formatMins(totalMins))}`);
      line();
    }
  )

  // GOAL
  .command(
    'goal [minutes]',
    'Set or check your daily goal (default 60 min)',
    (y) => y.positional('minutes', { type: 'number' }),
    (argv) => {
      const data = loadData();

      if (argv.minutes) {
        if (argv.minutes < 1 || argv.minutes > 1440) {
          console.log(chalk.red('Goal must be between 1 and 1440 minutes.'));
          return;
        }
        data.dailyGoalMinutes = argv.minutes;
        saveData(data);
        line();
        console.log(chalk.green('Daily goal updated'));
        console.log(`Goal  ${chalk.bold(formatMins(argv.minutes))} per day`);
        line();
        return;
      }

      const goal = data.dailyGoalMinutes || 60;
      const today = getTodayKey();
      const done = getTodayTotal(data.sessions, today);
      const remaining = Math.max(0, goal - done);
      const pct = getGoalPercent(done, goal);

      line();
      console.log(chalk.bold('Daily goal'));
      console.log('');
      console.log(`Goal       ${chalk.bold(formatMins(goal))}`);
      console.log(`Done       ${chalk.bold(formatMins(done))}  (${pct}%)`);
      console.log(
        `Remaining  ${remaining > 0 ? chalk.yellow(formatMins(remaining)) : chalk.green('Complete')}`
      );
      if (done >= goal) {
        console.log('');
        console.log(chalk.green('Goal complete. Great work today.'));
      }
      line();
    }
  )

  // HISTORY
  .command(
    'history [limit]',
    'Show the last N individual sessions (default 10)',
    (y) => y.positional('limit', { type: 'number', default: 10 }),
    (argv) => {
      const data = loadData();

      if (data.sessions.length === 0) {
        console.log(chalk.dim('No sessions recorded yet.'));
        return;
      }

      const limit = Math.max(1, argv.limit);
      const recent = data.sessions.slice(-limit).reverse();

      line();
      console.log(chalk.bold(`Last ${recent.length} sessions`));
      console.log('');

      for (const s of recent) {
        const start = new Date(s.startTime).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        });
        const end = new Date(s.endTime).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        });
        console.log(
          `  ${chalk.dim(s.date)}  ${chalk.bold(s.topic.padEnd(20))}  ${formatMins(s.durationMinutes).padStart(5)}  ${chalk.dim(start + ' - ' + end)}`
        );
      }
      line();
    }
  )

  // RESET
  .command(
    'reset',
    'Clear all session data (cannot be undone)',
    {},
    () => {
      const data = loadData();
      const count = data.sessions.length;
      data.sessions = [];
      data.currentSession = null;
      saveData(data);

      line();
      console.log(chalk.yellow('Data cleared'));
      console.log(`Removed ${count} session${count !== 1 ? 's' : ''}`);
      line();
    }
  )

  .scriptName('study')
  .usage('Usage: $0 <command> [options]')
  .help()
  .alias('h', 'help')
  .demandCommand(1, 'Please provide a command. Run study --help to see options.')
  .strict()
  .argv;
