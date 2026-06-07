import { describe, it, expect } from 'vitest';
import {
  formatDuration,
  formatMins,
  getTodayKey,
  getDateKey,
  getTodayTotal,
  getGoalPercent,
  buildSessionRecord,
  calcCurrentStreak,
  calcLongestStreak,
  groupByDate,
  groupByTopic,
  pickMotivation,
  MOTIVATIONS,
  getDataFilePath,
} from '../helpers.js';

// ─── Shared fixtures ───────────────────────────────────────────────────────

const NOW = new Date('2026-04-04T12:00:00.000Z');

function makeSession(date, topic, durationMinutes) {
  const start = new Date(`${date}T08:00:00.000Z`);
  const end = new Date(start.getTime() + durationMinutes * 60000);
  return {
    date,
    topic,
    startTime: start.toISOString(),
    endTime: end.toISOString(),
    durationMinutes,
  };
}

// ─── formatDuration ────────────────────────────────────────────────────────

describe('formatDuration', () => {
  it('shows seconds only when under a minute', () => {
    expect(formatDuration(45000)).toBe('45s');
  });

  it('shows minutes and seconds when under an hour', () => {
    expect(formatDuration(90000)).toBe('1m 30s');
  });

  it('shows hours, minutes, and seconds when over an hour', () => {
    expect(formatDuration(3661000)).toBe('1h 1m 1s');
  });

  it('handles exactly 0ms', () => {
    expect(formatDuration(0)).toBe('0s');
  });

  it('handles exactly 1 hour', () => {
    expect(formatDuration(3600000)).toBe('1h 0m 0s');
  });
});

// ─── formatMins ───────────────────────────────────────────────────────────

describe('formatMins', () => {
  it('shows minutes only when under an hour', () => {
    expect(formatMins(45)).toBe('45m');
  });

  it('shows hours only when evenly divisible', () => {
    expect(formatMins(120)).toBe('2h');
  });

  it('shows hours and minutes', () => {
    expect(formatMins(90)).toBe('1h 30m');
  });

  it('handles 0 minutes', () => {
    expect(formatMins(0)).toBe('0m');
  });
});

// ─── getTodayKey ──────────────────────────────────────────────────────────

describe('getTodayKey', () => {
  it('returns ISO date string YYYY-MM-DD', () => {
    const key = getTodayKey(NOW);
    expect(key).toBe('2026-04-04');
  });

  it('uses current date when no argument provided', () => {
    const key = getTodayKey();
    expect(key).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });
});

// ─── getDateKey ───────────────────────────────────────────────────────────

describe('getDateKey', () => {
  it('returns today with offset 0', () => {
    expect(getDateKey(0, NOW)).toBe('2026-04-04');
  });

  it('returns yesterday with offset 1', () => {
    expect(getDateKey(1, NOW)).toBe('2026-04-03');
  });

  it('returns 6 days ago with offset 6', () => {
    expect(getDateKey(6, NOW)).toBe('2026-03-29');
  });
});

// ─── getTodayTotal ────────────────────────────────────────────────────────

describe('getTodayTotal', () => {
  const sessions = [
    makeSession('2026-04-04', 'Math', 60),
    makeSession('2026-04-04', 'English', 30),
    makeSession('2026-04-03', 'Physics', 90),
  ];

  it('sums only sessions matching the given date', () => {
    expect(getTodayTotal(sessions, '2026-04-04')).toBe(90);
  });

  it('returns 0 when no sessions match', () => {
    expect(getTodayTotal(sessions, '2026-04-01')).toBe(0);
  });

  it('returns 0 for an empty array', () => {
    expect(getTodayTotal([], '2026-04-04')).toBe(0);
  });
});

// ─── getGoalPercent ───────────────────────────────────────────────────────

describe('getGoalPercent', () => {
  it('returns 50 when halfway there', () => {
    expect(getGoalPercent(30, 60)).toBe(50);
  });

  it('returns 100 when goal exactly met', () => {
    expect(getGoalPercent(60, 60)).toBe(100);
  });

  it('caps at 100 when goal exceeded', () => {
    expect(getGoalPercent(120, 60)).toBe(100);
  });

  it('returns 0 when nothing done', () => {
    expect(getGoalPercent(0, 60)).toBe(0);
  });

  it('returns 0 when goal is 0 to avoid division by zero', () => {
    expect(getGoalPercent(60, 0)).toBe(0);
  });
});

// ─── buildSessionRecord ───────────────────────────────────────────────────

describe('buildSessionRecord', () => {
  const start = new Date('2026-04-04T08:00:00.000Z');
  const end   = new Date('2026-04-04T09:30:00.000Z');

  const currentSession = {
    startTime: start.toISOString(),
    topic: 'Algorithms',
  };

  it('calculates durationMinutes correctly (90 min)', () => {
    const record = buildSessionRecord(currentSession, end);
    expect(record.durationMinutes).toBe(90);
  });

  it('sets durationMs to the exact millisecond difference', () => {
    const record = buildSessionRecord(currentSession, end);
    expect(record.durationMs).toBe(end - start);
  });

  it('preserves the topic', () => {
    const record = buildSessionRecord(currentSession, end);
    expect(record.topic).toBe('Algorithms');
  });

  it('sets endTime to the end date ISO string', () => {
    const record = buildSessionRecord(currentSession, end);
    expect(record.endTime).toBe(end.toISOString());
  });

  it('floors very short sessions to 1 minute minimum', () => {
    const almostNow = new Date(start.getTime() + 5000); // 5 seconds
    const record = buildSessionRecord(currentSession, almostNow);
    expect(record.durationMinutes).toBe(1);
  });
});

// ─── groupByDate ─────────────────────────────────────────────────────────

describe('groupByDate', () => {
  it('sums minutes per date', () => {
    const sessions = [
      makeSession('2026-04-04', 'Math', 60),
      makeSession('2026-04-04', 'English', 45),
      makeSession('2026-04-03', 'Physics', 30),
    ];
    const result = groupByDate(sessions);
    expect(result['2026-04-04']).toBe(105);
    expect(result['2026-04-03']).toBe(30);
  });

  it('returns an empty object for no sessions', () => {
    expect(groupByDate([])).toEqual({});
  });
});

// ─── groupByTopic ─────────────────────────────────────────────────────────

describe('groupByTopic', () => {
  it('sums minutes per topic across dates', () => {
    const sessions = [
      makeSession('2026-04-04', 'Math', 60),
      makeSession('2026-04-03', 'Math', 30),
      makeSession('2026-04-04', 'English', 45),
    ];
    const result = groupByTopic(sessions);
    expect(result['Math']).toBe(90);
    expect(result['English']).toBe(45);
  });

  it('returns an empty object for no sessions', () => {
    expect(groupByTopic([])).toEqual({});
  });
});

// ─── calcCurrentStreak ────────────────────────────────────────────────────

describe('calcCurrentStreak', () => {
  const goal = 60;

  it('returns 0 when today has no sessions', () => {
    const sessions = [makeSession('2026-04-03', 'Math', 90)];
    expect(calcCurrentStreak(sessions, goal, NOW)).toBe(0);
  });

  it('returns 1 when only today meets the goal', () => {
    const sessions = [makeSession('2026-04-04', 'Math', 90)];
    expect(calcCurrentStreak(sessions, goal, NOW)).toBe(1);
  });

  it('counts consecutive days ending today', () => {
    const sessions = [
      makeSession('2026-04-02', 'Math', 90),
      makeSession('2026-04-03', 'Math', 90),
      makeSession('2026-04-04', 'Math', 90),
    ];
    expect(calcCurrentStreak(sessions, goal, NOW)).toBe(3);
  });

  it('breaks the streak on a missed day', () => {
    const sessions = [
      makeSession('2026-04-01', 'Math', 90), // gap here
      makeSession('2026-04-03', 'Math', 90),
      makeSession('2026-04-04', 'Math', 90),
    ];
    expect(calcCurrentStreak(sessions, goal, NOW)).toBe(2);
  });

  it('does not count a day where the goal was not reached', () => {
    const sessions = [
      makeSession('2026-04-03', 'Math', 30), // below goal
      makeSession('2026-04-04', 'Math', 90),
    ];
    expect(calcCurrentStreak(sessions, goal, NOW)).toBe(1);
  });
});

// ─── calcLongestStreak ────────────────────────────────────────────────────

describe('calcLongestStreak', () => {
  const goal = 60;

  it('returns 0 for no sessions', () => {
    expect(calcLongestStreak([], goal)).toBe(0);
  });

  it('returns 1 for a single qualifying day', () => {
    const sessions = [makeSession('2026-04-04', 'Math', 90)];
    expect(calcLongestStreak(sessions, goal)).toBe(1);
  });

  it('finds a longer run in history even when current streak is shorter', () => {
    const sessions = [
      // Old 5-day streak
      makeSession('2026-03-10', 'Math', 90),
      makeSession('2026-03-11', 'Math', 90),
      makeSession('2026-03-12', 'Math', 90),
      makeSession('2026-03-13', 'Math', 90),
      makeSession('2026-03-14', 'Math', 90),
      // Current 2-day streak
      makeSession('2026-04-03', 'Math', 90),
      makeSession('2026-04-04', 'Math', 90),
    ];
    expect(calcLongestStreak(sessions, goal)).toBe(5);
  });

  it('ignores days that do not meet the goal', () => {
    const sessions = [
      makeSession('2026-04-01', 'Math', 20), // below goal, breaks streak
      makeSession('2026-04-02', 'Math', 90),
      makeSession('2026-04-03', 'Math', 90),
    ];
    expect(calcLongestStreak(sessions, goal)).toBe(2);
  });
});

// ─── pickMotivation ───────────────────────────────────────────────────────

describe('pickMotivation', () => {
  it('returns an object with text and url properties', () => {
    const m = pickMotivation(0);
    expect(m).toHaveProperty('text');
    expect(m).toHaveProperty('url');
  });

  it('returns different items for different indexes', () => {
    const m0 = pickMotivation(0);
    const m1 = pickMotivation(1);
    expect(m0.text).not.toBe(m1.text);
  });

  it('wraps around when index exceeds array length', () => {
    const m = pickMotivation(MOTIVATIONS.length);
    expect(m).toEqual(MOTIVATIONS[0]);
  });

  it('returns a result within bounds for random pick', () => {
    const m = pickMotivation();
    expect(MOTIVATIONS).toContainEqual(m);
  });

  it('some motivations have a url and some do not', () => {
    const withUrl = MOTIVATIONS.filter((m) => m.url !== null);
    const withoutUrl = MOTIVATIONS.filter((m) => m.url === null);
    expect(withUrl.length).toBeGreaterThan(0);
    expect(withoutUrl.length).toBeGreaterThan(0);
  });
});

// ─── getDataFilePath ──────────────────────────────────────────────────────

describe('getDataFilePath', () => {
  it('ends with study-log.json', () => {
    expect(getDataFilePath()).toMatch(/study-log\.json$/);
  });

  it('contains Documents in the path', () => {
    expect(getDataFilePath()).toMatch(/Documents/);
  });

  it('is an absolute path', () => {
    const p = getDataFilePath();
    // Absolute on Windows starts with a drive letter, on Unix with /
    const isAbsolute = p.startsWith('/') || /^[A-Za-z]:\\/.test(p);
    expect(isAbsolute).toBe(true);
  });
});
