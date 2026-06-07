'use strict';

const os = require('os');
const path = require('path');

// ─── Data file path ────────────────────────────────────────────────────────
// Always stored in the user's Documents folder so it survives terminal changes.

function getDataFilePath() {
  const home = os.homedir();
  // Works on Windows (C:\Users\Name\Documents) and Mac/Linux (~/Documents)
  return path.join(home, 'Documents', 'study-log.json');
}

// ─── Date helpers ──────────────────────────────────────────────────────────

function getTodayKey(now = new Date()) {
  return now.toISOString().split('T')[0];
}

function getDateKey(offsetDays = 0, now = new Date()) {
  const d = new Date(now);
  d.setDate(d.getDate() - offsetDays);
  return d.toISOString().split('T')[0];
}

// ─── Formatting ────────────────────────────────────────────────────────────

function formatDuration(ms) {
  const totalSecs = Math.floor(ms / 1000);
  const h = Math.floor(totalSecs / 3600);
  const m = Math.floor((totalSecs % 3600) / 60);
  const s = totalSecs % 60;
  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

function formatMins(mins) {
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  if (h > 0 && m > 0) return `${h}h ${m}m`;
  if (h > 0) return `${h}h`;
  return `${m}m`;
}

// ─── Session calculations ──────────────────────────────────────────────────

function getTodayTotal(sessions, todayKey) {
  return sessions
    .filter((s) => s.date === todayKey)
    .reduce((sum, s) => sum + s.durationMinutes, 0);
}

function getGoalPercent(doneMins, goalMins) {
  if (goalMins <= 0) return 0;
  return Math.min(100, Math.round((doneMins / goalMins) * 100));
}

function buildSessionRecord(currentSession, endTime) {
  const start = new Date(currentSession.startTime);
  const durationMs = endTime - start;
  const durationMins = Math.max(1, Math.round(durationMs / 60000));
  return {
    date: getTodayKey(endTime),
    topic: currentSession.topic,
    startTime: currentSession.startTime,
    endTime: endTime.toISOString(),
    durationMinutes: durationMins,
    durationMs,
  };
}

// ─── Streak calculation ────────────────────────────────────────────────────

function calcCurrentStreak(sessions, goalMins, now = new Date()) {
  const byDate = groupByDate(sessions);
  let streak = 0;
  let i = 0;
  while (true) {
    const key = getDateKey(i, now);
    if ((byDate[key] || 0) >= goalMins) {
      streak++;
      i++;
    } else {
      break;
    }
  }
  return streak;
}

function calcLongestStreak(sessions, goalMins) {
  const byDate = groupByDate(sessions);
  const qualifyingDates = Object.keys(byDate)
    .filter((d) => byDate[d] >= goalMins)
    .sort();

  let longest = 0;
  let run = 0;
  let prev = null;

  for (const d of qualifyingDates) {
    if (prev) {
      const diff = (new Date(d) - new Date(prev)) / 86400000;
      run = diff === 1 ? run + 1 : 1;
    } else {
      run = 1;
    }
    longest = Math.max(longest, run);
    prev = d;
  }
  return longest;
}

// ─── Grouping helpers ──────────────────────────────────────────────────────

function groupByDate(sessions) {
  const map = {};
  for (const s of sessions) {
    map[s.date] = (map[s.date] || 0) + s.durationMinutes;
  }
  return map;
}

function groupByTopic(sessions) {
  const map = {};
  for (const s of sessions) {
    map[s.topic] = (map[s.topic] || 0) + s.durationMinutes;
  }
  return map;
}

// ─── Motivation ────────────────────────────────────────────────────────────

const MOTIVATIONS = [
  {
    text: 'Every minute counts. Keep going.',
    url: 'https://youtu.be/KxGRhd_iWuE',
  },
  {
    text: 'Consistency beats intensity. You are building a habit.',
    url: 'https://youtu.be/KxGRhd_iWuE',
  },
  {
    text: 'Great focus. Your future self will thank you.',
    url: null,
  },
  {
    text: 'Learning is a journey and you are moving forward.',
    url: null,
  },
  {
    text: 'Small steps compound. You are doing great.',
    url: 'https://youtu.be/KxGRhd_iWuE',
  },
  {
    text: 'Another session in the books. Well done.',
    url: null,
  },
  {
    text: 'Discipline is the bridge between goals and accomplishment.',
    url: null,
  },
];

function pickMotivation(index = null) {
  const i = index !== null ? index : Math.floor(Math.random() * MOTIVATIONS.length);
  return MOTIVATIONS[i % MOTIVATIONS.length];
}

module.exports = {
  getDataFilePath,
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
  MOTIVATIONS,
};
