# Study Timer CLI

A command-line tool to track study sessions, monitor daily goals, and stay consistent. Data is saved to your Documents folder so it is always in the same place no matter which terminal or folder you open.

---

## Requirements

- Node.js v16 or higher
- npm

---

## Installation

```bash
# 1. Enter the project folder
cd study-timer

# 2. Install dependencies
npm install

# 3. Link globally so you can type "study" from anywhere
npm link
```

After `npm link`, type `study` from any terminal window. If you skip this step, replace `study` with `node cli.js` in all examples below.

---

## Data file location

Your sessions are always saved to:

| OS | Path |
|----|------|
| Windows | `C:\Users\YourName\Documents\study-log.json` |
| macOS | `/Users/YourName/Documents/study-log.json` |
| Linux | `/home/YourName/Documents/study-log.json` |

The path is shown every time you run `study start`. The file is plain JSON so you can open it in any text editor, back it up to OneDrive, or sync it with Git.

---

## Motivation links

When you start a session, a motivational message is shown. Some messages also open a YouTube link in your default browser automatically. You can edit the `MOTIVATIONS` array in `helpers.js` to add your own messages and links.

```js
const MOTIVATIONS = [
  { text: 'Every minute counts. Keep going.', url: 'https://youtu.be/KxGRhd_iWuE' },
  { text: 'Great focus. Your future self will thank you.', url: null },
  // Add your own here
];
```

Set `url` to a YouTube link or any URL to open it on start. Set `url` to `null` to show text only.

---

## Commands

### `study start [topic]`

Start a new session. Shows a motivation message and opens a link if one is attached.

```
study start Math
study start "Linear Algebra"
study start
```

---

### `study stop`

Stop the active session. Saves it and shows duration, today's total, and goal progress.

```
study stop
```

---

### `study status`

Check if a session is active, how long it has been running, and today's total.

```
study status
```

---

### `study review [days]`

Day-by-day summary for the last N days (default 7, max 30). Days where the goal was met are highlighted.

```
study review
study review 14
```

---

### `study streak`

Shows your current streak (consecutive days meeting the goal) and your all-time longest streak.

```
study streak
```

---

### `study topics`

Total time per topic across all sessions, sorted from most to least.

```
study topics
```

---

### `study goal [minutes]`

Set your daily goal in minutes, or check today's progress. Default is 60 minutes.

```
study goal          # check today
study goal 90       # set to 90 min
```

---

### `study history [limit]`

Last N individual sessions with date, topic, duration, and time range. Default 10.

```
study history
study history 20
```

---

### `study reset`

Deletes all session data. Cannot be undone.

```
study reset
```

---

## How it works

`study start` saves the current timestamp and topic to the JSON file. `study stop` reads that timestamp and computes the elapsed time. No process runs in the background — your terminal can close or crash and nothing is lost.

### JSON structure

```json
{
  "currentSession": {
    "startTime": "2026-04-04T07:00:00.000Z",
    "topic": "Math"
  },
  "dailyGoalMinutes": 90,
  "sessions": [
    {
      "date": "2026-04-03",
      "topic": "Physics",
      "startTime": "2026-04-03T09:00:00.000Z",
      "endTime": "2026-04-03T10:00:00.000Z",
      "durationMinutes": 60
    }
  ]
}
```

`currentSession` is `null` when no session is active.

---

## Testing

Tests are written with [Vitest](https://vitest.dev/) and cover all pure logic in `helpers.js`. No file system is touched during tests.

```bash
# Run all tests once
npm test

# Watch mode (re-runs on file save)
npm run test:watch
```

The test file is at `tests/helpers.test.js`. It covers formatting, date helpers, session calculations, streak logic, grouping, motivation picking, and the data file path.

---

## Project structure

```
study-timer/
  cli.js          # commands and terminal output
  helpers.js      # pure logic — formatting, calculations, streak math
  store.js        # file read/write, isolated for easy testing
  tests/
    helpers.test.js
  vitest.config.js
  package.json
  README.md
```

---

## Dependencies

- [yargs](https://github.com/yargs/yargs) — command parsing
- [chalk](https://github.com/chalk/chalk) — terminal colors

### Dev dependencies

- [vitest](https://vitest.dev/) — test runner
