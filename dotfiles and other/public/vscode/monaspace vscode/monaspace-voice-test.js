// ─────────────────────────────────────────────────────────────────
// MONASPACE VOICE TEST — GitHub Dark Default
// Each line is labeled with what font you should see.
// Open this file in VS Code with the CSS injected and verify.
// ─────────────────────────────────────────────────────────────────
//
// RADON   → this comment block. Handwritten, italic, light weight.
//           If this looks identical to code below, CSS isn't loaded.
//           Run: Ctrl+Shift+P → "Enable Custom CSS and JS" → restart.


// ── 1. XENON: keywords (red in GitHub Dark) ──────────────────────
//    if · else · for · while · return · class · function
//    const · let · var · import · export · async · await · new

const greeting = "hello";          // const → XENON, "hello" → ARGON
let count = 0;                      // let   → XENON, 0 → KRYPTON
var legacy = true;                  // var   → XENON, true → KRYPTON

class Animal {                      // class → XENON, Animal → XENON (lighter)
  constructor(name, legs) {         // name, legs → NEON
    this.name = name;               // this → XENON, .name → NEON
    this.legs = legs;
  }
}

async function fetchUser(id) {      // async function → XENON, fetchUser → NEON↑, id → NEON
  if (id <= 0) return null;         // if return → XENON, 0 → KRYPTON, null → KRYPTON
  try {                             // try → XENON
    const data = await getUser(id); // const await → XENON, data → NEON, getUser → NEON↑
    return data;                    // return → XENON
  } catch (err) {                   // catch → XENON
    throw new Error(err.message);   // throw new → XENON, Error → NEON↑
  }
}


// ── 2. ARGON: strings (light blue + green in GitHub Dark) ────────

const plain    = "double quoted string";         // ARGON
const single   = 'single quoted string';         // ARGON
const template = `template literal ${count}`;   // backtick → ARGON, ${count} → NEON
const html     = "<div class=\"app\">hello</div>"; // ARGON throughout
const escaped  = "tab:\there\nnewline";          // escape sequences → ARGON
const regex    = /^https?:\/\/[\w.-]+/gi;        // regex → ARGON (green in theme)
const tagged   = String.raw`C:\Users\dev\file`;  // tagged template → ARGON


// ── 3. KRYPTON: numbers, booleans, null, operators ───────────────

const integer   = 42;              // KRYPTON
const float     = 3.14159;         // KRYPTON
const negative  = -273.15;         // KRYPTON
const hex       = 0xff00cc;        // KRYPTON
const binary    = 0b1010_1100;     // KRYPTON
const bigint    = 9007199254740991n; // KRYPTON
const yes       = true;            // KRYPTON
const no        = false;           // KRYPTON
const nothing   = null;            // KRYPTON
const empty     = undefined;       // KRYPTON

// Operators — all should render in KRYPTON
const math      = (10 + 5 - 3) * 4 / 2 % 7; // + - * / % → KRYPTON
const compare   = count >= 0 && count <= 100; // >= <= && → KRYPTON
const nullish   = greeting ?? "fallback";      // ?? → KRYPTON
const optional  = greeting?.length;            // ?. → KRYPTON
const spread    = [...[1, 2, 3]];              // ... → KRYPTON
const strict    = (1 === 1) !== false;         // === !== → KRYPTON
const bitwise   = 0b1010 & 0b1100 | 0b0001;  // & | → KRYPTON


// ── 4. NEON: identifiers and variables (blue in GitHub Dark) ──────

const userName   = "alice";        // userName → NEON
const userAge    = 30;             // userAge → NEON
const userActive = true;           // userActive → NEON

const obj = {
  id:    1,                        // id → NEON (property key)
  name:  "bob",                    // name → NEON, "bob" → ARGON
  score: 98.6,                     // score → NEON, 98.6 → KRYPTON
  tags:  ["js", "php"],            // tags → NEON, "js"/"php" → ARGON
};

const { id, name, score } = obj;   // destructured → NEON
const [first, ...rest] = [1,2,3];  // first rest → NEON


// ── 5. NEON (elevated weight): function names (purple in theme) ───

function add(a, b) {               // add → NEON↑ (heavier), a b → NEON
  return a + b;
}

const multiply = (x, y) => x * y; // multiply → NEON, x y → NEON

class Calculator extends Animal {  // Calculator → XENON lighter, extends → XENON
  static #precision = 2;           // static → XENON, #precision → NEON

  add(a, b) {                      // add → NEON↑ (method name, purple)
    return parseFloat(             // parseFloat → NEON↑
      (a + b).toFixed(this.#precision) // toFixed → NEON↑
    );
  }

  get value() { return this._v; }  // get → XENON, value → NEON↑
  set value(v) { this._v = v; }    // set → XENON, value → NEON↑
}


// ── 6. XENON (lighter): class names and types ─────────────────────

class UserService {}               // UserService → XENON lighter (gold in theme)
class ApiController {}             // ApiController → XENON lighter
class HttpError extends Error {}   // HttpError ApiController → XENON lighter


// ── 7. KRYPTON: keyword-operators (typeof delete instanceof) ──────
//    These get a slightly different shade in GitHub Dark

const type    = typeof count;      // typeof → KRYPTON
const cleared = delete obj.score;  // delete → KRYPTON
const isArr   = [] instanceof Array; // instanceof → KRYPTON
const keys    = Object.keys(obj);  // in pattern: for (k in obj) → KRYPTON


// ── 8. RADON: comments in all forms ───────────────────────────────

// Single-line comment — RADON. Handwritten, italic, clearly not code.

/*
 * Multi-line block comment — RADON.
 * Every line should look like a handwritten annotation.
 * Compare the letter shapes here vs the code above.
 */

/**
 * JSDoc comment — RADON for prose, but type refs stay upright.
 * @param  {string}  name  - user's display name    ← RADON
 * @param  {number}  age   - user's age in years    ← RADON
 * @returns {Object}       - user record             ← RADON
 */
function createUser(name, age) {
  // Inline comment mid-function — RADON
  return { name, age, createdAt: Date.now() }; // → KRYPTON (Date.now number result)
}


// ── 9. MIXED: all voices on adjacent lines ─────────────────────────
//    This is the real test. Scan down and check the rhythm.

import { readFile } from "fs/promises";   // import from → XENON, "fs/promises" → ARGON

const MAX_RETRIES = 3;                     // const → XENON, MAX_RETRIES → NEON, 3 → KRYPTON

async function loadConfig(path) {          // async function → XENON, loadConfig → NEON↑
  // Attempt to read config file           ← RADON
  for (let i = 0; i < MAX_RETRIES; i++) { // for let → XENON, 0 MAX_RETRIES → KRYPTON
    try {
      const raw  = await readFile(path, "utf-8"); // const await → XENON, "utf-8" → ARGON
      const data = JSON.parse(raw);               // JSON → NEON↑, parse → NEON↑
      return data ?? {};                          // return → XENON, {} → KRYPTON, ?? → KRYPTON
    } catch {
      if (i === MAX_RETRIES - 1) throw new Error(`Failed after ${MAX_RETRIES} retries`);
      // ↑ if → XENON, MAX_RETRIES → NEON, 1 → KRYPTON, throw new → XENON, Error → NEON↑
      // ↑ template string → ARGON, ${MAX_RETRIES} → NEON, "retries" → ARGON
    }
  }
}


// ── 10. COPILOT GHOST TEXT CHECK ──────────────────────────────────
// Start typing an incomplete function below and accept a suggestion.
// The ghost text (grey autocomplete) should appear in KRYPTON:
// mechanical, lighter weight, reduced opacity.

function reverseString(str) {
  // type something here and watch for Copilot suggestion in Krypton

}


// ─────────────────────────────────────────────────────────────────
// WHAT TO CHECK IF A VOICE LOOKS WRONG
// ─────────────────────────────────────────────────────────────────
// 1. Open DevTools: Help → Toggle Developer Tools
// 2. Click inspector icon (top-left of DevTools panel)
// 3. Click the token that's wrong in the editor
// 4. Note the .mtkN class on the <span>
// 5. Find that color in the quick-reference table at the bottom
//    of monaspace.css and update the rule to match your class number
// ─────────────────────────────────────────────────────────────────
