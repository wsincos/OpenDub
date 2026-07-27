#!/usr/bin/env node
/** Capture the real V3 browser interactions used by the narrated evidence film. */
import { mkdir, rename } from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.OPENDUB_WEB_URL ?? "http://127.0.0.1:5181";
const outputDirectory = path.resolve("docs/grant/video/v3/assets/browser-captures");
const viewport = { width: 1920, height: 1080 };

const caseDefinitions = [
  {
    id: "human-0",
    tab: /human portrait/i,
    displayName: "Human portrait case",
  },
  {
    id: "animation-1",
    tab: /animated character/i,
    displayName: "Animated character case",
  },
];

const artifacts = [
  { file: "gt.mp4", label: "Ground truth", stem: "gt" },
  { file: "hpmdubbing.mp4", label: "HPMDubbing", stem: "hpmdubbing" },
  { file: "styledubber.mp4", label: "StyleDubber", stem: "styledubber" },
  { file: "emodubber.mp4", label: "EmoDubber", stem: "emodubber" },
];

async function waitForVisible(page, locator) {
  await locator.waitFor({ state: "visible" });
  await locator.scrollIntoViewIfNeeded();
}

async function ensureArtifactPlayback(page, video, audibleLabel) {
  await video.click({ position: { x: 90, y: 70 } });
  const status = page.getByText(audibleLabel, { exact: true });
  try {
    await status.waitFor({ state: "visible", timeout: 1000 });
  } catch {
    await video.evaluate(async (element) => {
      element.muted = true;
      await element.play();
    });
  }
  await status.waitFor({ state: "visible" });
}

const narratedScenarios = [
  {
    file: "01-identity-task-flow.webm",
    path: "/vtts?tour=flow",
    async perform(page) {
      await page.waitForTimeout(14_600);
    },
  },
  {
    file: "02-task-illustration.webm",
    path: "/vtts",
    async perform(page) {
      const panel = page.locator(".task-illustration");
      await waitForVisible(page, panel);
      await page.getByRole("button", { name: /hide lip overlay/i }).click();
      await page.waitForTimeout(600);
      await page.getByRole("button", { name: /show lip overlay/i }).click();
      await page.getByRole("button", { name: /play illustrated timeline/i }).click();
      await page.waitForTimeout(14_000);
    },
  },
  {
    file: "03-method-selection.webm",
    path: "/methods",
    async perform(page) {
      await page.getByRole("button", { name: /pronunciation and character style/i }).click();
      await page.waitForTimeout(6_000);
      await page.getByRole("button", { name: /explicit emotion direction/i }).click();
      await page.waitForTimeout(15_000);
    },
  },
  {
    file: "04-method-canvas.webm",
    path: "/methods/styledubber",
    async perform(page) {
      await page.getByRole("button", { name: "Signals" }).click();
      await page.getByRole("button", { name: /inspect/i }).nth(2).click();
      await page.waitForTimeout(2_000);
      await page.locator(".signal-chips button").first().click();
      await page.waitForTimeout(15_000);
    },
  },
  {
    file: "05-evidence-boundary.webm",
    path: "/evidence",
    async perform(page) {
      await page.getByRole("heading", { name: /evidence is part of the method/i }).scrollIntoViewIfNeeded();
      await page.waitForTimeout(15_000);
    },
  },
];

async function capture(browser, scenario) {
  const context = await browser.newContext({
    viewport,
    recordVideo: { dir: outputDirectory, size: viewport },
  });
  const page = await context.newPage();
  try {
    await page.goto(`${baseUrl}${scenario.path}`, { waitUntil: "networkidle" });
    await scenario.perform(page);
    const recordedPath = await page.video().path();
    await page.close();
    await context.close();
    await rename(recordedPath, path.join(outputDirectory, scenario.file));
    process.stdout.write(`captured ${scenario.file}\n`);
  } catch (error) {
    await context.close();
    throw error;
  }
}

async function main() {
  await mkdir(outputDirectory, { recursive: true });
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  try {
    for (const scenario of narratedScenarios) await capture(browser, scenario);
    for (const caseDefinition of caseDefinitions) {
      for (const artifact of artifacts) {
        await capture(browser, {
          file: `${caseDefinition.id}-${artifact.stem}.webm`,
          path: "/examples",
          async perform(page) {
            await page.getByRole("tab", { name: caseDefinition.tab }).click();
            const video = page.getByLabel(`${caseDefinition.displayName}, ${artifact.label}`);
            await waitForVisible(page, video);
            await ensureArtifactPlayback(page, video, `AUDIBLE: ${artifact.label}`);
            await page.waitForTimeout(3_000);
          },
        });
      }
    }
  } finally {
    await browser.close();
  }
}

await main();
