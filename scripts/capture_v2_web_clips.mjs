#!/usr/bin/env node
/**
 * Capture the V2 interaction clips used by the grant film.
 *
 * Start the Vite server first, then run `pnpm exec playwright install ffmpeg`
 * once for the local Playwright version and invoke this script.
 */
import { rename } from "node:fs/promises";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.OPENDUB_WEB_URL ?? "http://127.0.0.1:5181";
const outputDirectory = path.resolve("docs/grant/video/v2/assets/clips");
const viewport = { width: 1920, height: 1080 };

const scenarios = [
  {
    file: "01-task-flow.webm",
    path: "/vtts?tour=flow",
    async perform(page) {
      await page.waitForTimeout(7200);
    },
  },
  {
    file: "02-cue-microscope.webm",
    path: "/vtts",
    async perform(page) {
      await page.locator(".cue-microscope").scrollIntoViewIfNeeded();
      await page.waitForTimeout(1000);
      for (const label of ["Lip cue", "Environment cue", "Face cue"]) {
        await page.getByRole("button", { name: label }).click();
        await page.waitForTimeout(1100);
      }
    },
  },
  {
    file: "03-shared-timeline.webm",
    path: "/vtts",
    async perform(page) {
      await page.locator(".sync-timeline").scrollIntoViewIfNeeded();
      const slider = page.getByRole("slider", { name: "Synchronized task time" });
      await page.waitForTimeout(900);
      for (const value of [12, 47, 82]) {
        await slider.evaluate((element, next) => {
          const input = element;
          input.value = String(next);
          input.dispatchEvent(new Event("input", { bubbles: true }));
          input.dispatchEvent(new Event("change", { bubbles: true }));
        }, value);
        await page.waitForTimeout(1300);
      }
    },
  },
];

await mkdir(outputDirectory, { recursive: true });
const browser = await chromium.launch({ channel: "chrome", headless: true });

try {
  for (const scenario of scenarios) {
    const context = await browser.newContext({
      viewport,
      recordVideo: { dir: outputDirectory, size: viewport },
    });
    const page = await context.newPage();
    await page.goto(`${baseUrl}${scenario.path}`, { waitUntil: "networkidle" });
    await scenario.perform(page);
    const recordedPath = await page.video().path();
    await page.close();
    await context.close();
    await rename(recordedPath, path.join(outputDirectory, scenario.file));
    process.stdout.write(`captured ${scenario.file}\n`);
  }
} finally {
  await browser.close();
}
