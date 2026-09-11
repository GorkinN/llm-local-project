#!/usr/bin/env node

import { spawn, execSync } from "node:child_process";
import puppeteer from "puppeteer-core";
import { existsSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";

const useProfile = process.argv[2] === "--profile";

if (process.argv[2] && process.argv[2] !== "--profile") {
  console.log("Usage: browser-start.js [--profile]");
  console.log("\nOptions:");
  console.log(
    "  --profile  Copy your default Chrome profile (cookies, logins)",
  );
  process.exit(1);
}

const SCRAPING_DIR = path.join(
  process.env.USERPROFILE || process.env.HOME,
  ".cache",
  "browser-tools",
);

// Check if already running on :9222
try {
  const browser = await puppeteer.connect({
    browserURL: "http://localhost:9222",
    defaultViewport: null,
  });
  await browser.disconnect();
  console.log("✓ Chrome already running on :9222");
  process.exit(0);
} catch {}

// Setup profile directory
if (!existsSync(SCRAPING_DIR)) {
  mkdirSync(SCRAPING_DIR, { recursive: true });
}

// Remove SingletonLock to allow new instance
try {
  rmSync(path.join(SCRAPING_DIR, "SingletonLock"), { force: true });
  rmSync(path.join(SCRAPING_DIR, "SingletonSocket"), { force: true });
  rmSync(path.join(SCRAPING_DIR, "SingletonCookie"), { force: true });
} catch {}

// Find Chrome executable
const chromePath =
  process.env.CHROME_BIN ||
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

if (!existsSync(chromePath)) {
  console.error(`✗ Chrome not found at: ${chromePath}`);
  console.error("Set CHROME_BIN environment variable to your Chrome location");
  process.exit(1);
}

if (useProfile) {
  console.log(
    "Note: --profile flag copies your Chrome profile. This may not work perfectly on Windows.",
  );
  console.log(
    "For better results, close Chrome first and use your actual profile directory.",
  );
  // On Windows, we'll use the actual Chrome profile directory
  const userDataDir = path.join(
    process.env.USERPROFILE,
    "AppData",
    "Local",
    "Google",
    "Chrome",
    "User Data",
  );
  startChrome(chromePath, userDataDir);
} else {
  startChrome(chromePath, SCRAPING_DIR);
}

function startChrome(chromePath, userDataDir) {
  // Start Chrome with flags
  spawn(
    chromePath,
    [
      "--remote-debugging-port=9222",
      `--user-data-dir=${userDataDir}`,
      "--no-first-run",
      "--no-default-browser-check",
    ],
    { detached: true, stdio: "ignore" },
  ).unref();
}

// Wait for Chrome to be ready
let connected = false;
for (let i = 0; i < 30; i++) {
  try {
    const browser = await puppeteer.connect({
      browserURL: "http://localhost:9222",
      defaultViewport: null,
    });
    await browser.disconnect();
    connected = true;
    break;
  } catch {
    await new Promise((r) => setTimeout(r, 500));
  }
}

if (!connected) {
  console.error("✗ Failed to connect to Chrome");
  process.exit(1);
}

console.log(
  `✓ Chrome started on :9222${useProfile ? " with your profile" : ""}`,
);
