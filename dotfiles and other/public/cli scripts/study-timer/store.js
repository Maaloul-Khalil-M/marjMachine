'use strict';

const fs = require('fs');
const path = require('path');
const { getDataFilePath } = require('./helpers');

const DEFAULT_DATA = {
  currentSession: null,
  dailyGoalMinutes: 60,
  sessions: [],
};

function loadData(filePath = getDataFilePath()) {
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const parsed = JSON.parse(raw);
    // Merge with defaults so older files without new fields still work
    return { ...DEFAULT_DATA, ...parsed };
  } catch {
    return { ...DEFAULT_DATA };
  }
}

function saveData(data, filePath = getDataFilePath()) {
  // Ensure the directory exists (Documents folder always should, but just in case)
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

module.exports = { loadData, saveData, DEFAULT_DATA };
