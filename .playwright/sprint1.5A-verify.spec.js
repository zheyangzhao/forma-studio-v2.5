let test;
let expect;
try {
  ({ test, expect } = require('@playwright/test'));
} catch (err) {
  ({ test, expect } = require('playwright/test'));
}
const fs = require('fs');

test.use({
  headless: true,
  viewport: { width: 1280, height: 900 },
  actionTimeout: 5000,
  permissions: ['clipboard-read', 'clipboard-write'],
});

test('Sprint 1.5 §A — EvoLinkAI 整合驗證', async ({ page }) => {
  fs.mkdirSync('.playwright', { recursive: true });

  const errors = [];
  const failures = [];
  const stepStatus = [];
  const screenshotPath = step => `.playwright/sprint1.5A-verify-${String(step).padStart(2, '0')}.png`;

  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(`pageerror: ${err.message}`));

  async function snap(step) {
    await page.screenshot({ path: screenshotPath(step), fullPage: true }).catch(() => {});
  }

  async function runStep(step, description, fn) {
    try {
      await fn();
      await snap(step);
      stepStatus.push({ step, description, ok: true, screenshot: screenshotPath(step) });
    } catch (err) {
      await snap(step);
      const reason = err && err.message ? err.message.split('\n')[0] : String(err);
      failures.push({ step, description, reason, screenshot: screenshotPath(step) });
      stepStatus.push({ step, description, ok: false, reason, screenshot: screenshotPath(step) });
    }
  }

  async function visibleGalleryCount(section) {
    const countText = await section.locator('span', { hasText: /條符合 · 來源 CC BY 4\.0/ }).textContent();
    return Number((countText || '').match(/(\d+)\s+條符合/)?.[1]);
  }

  await runStep(1, 'goto HTML and verify FORMA_GALLERY globals', async () => {
    await page.goto('http://localhost:8765/forma-studio.html', { waitUntil: 'networkidle' });
    await expect(page).toHaveTitle(/Forma Studio/);

    const meta = await page.evaluate(() => ({
      total: window.FORMA_GALLERY?.total_count,
      cats: window.FORMA_GALLERY?.categories?.length,
      sources: (window.FORMA_GALLERY?.sources || []).map(s => s.repo).sort(),
    }));

    expect(meta.total).toBe(116);
    expect(meta.cats).toBe(17);
    expect(meta.sources).toEqual([
      'EvoLinkAI/awesome-gpt-image-2-prompts',
      'wuyoscar/gpt_image_2_skill',
    ]);
  });

  await runStep(2, 'count prompts with source.author', async () => {
    const authorCount = await page.evaluate(() => {
      const cats = window.FORMA_GALLERY?.categories || [];
      return cats.flatMap(c => c.prompts || []).filter(p => p.source?.author).length;
    });
    expect(authorCount).toBe(50);
  });

  await runStep(3, 'fill dummy API key, Section 1 description, and continue to Section 2', async () => {
    await page.getByRole('button', { name: /設定 API Key|設定 OpenAI API Key|API Key 已設定/ }).first().click();
    const input = page.locator('input[placeholder="sk-proj-..."]').last();
    await expect(input).toBeVisible();
    await input.fill('sk-test-dummy-not-real');
    await expect(input).toHaveValue('sk-test-dummy-not-real');
    await page.getByRole('button', { name: '儲存' }).last().click();

    const textarea = page.locator('#dt-step-1 textarea').first();
    await expect(textarea).toBeVisible();
    await textarea.fill('我要做一份行銷活動主視覺，用於新產品上市社群宣傳');
    await expect(textarea).toHaveValue('我要做一份行銷活動主視覺，用於新產品上市社群宣傳');

    await page.getByRole('button', { name: '繼續 → 設定受眾與基調' }).click();
    await expect(page.locator('#dt-step-2')).toHaveClass(/glow-active/);
  });

  await runStep(4, 'select marketing industry chip', async () => {
    const section = page.locator('#dt-step-2');
    const marketingChip = section.getByRole('button', { name: /行銷/ });
    await marketingChip.click();
    await expect(marketingChip).toHaveClass(/border-emerald-400/);
    await expect(section.getByText('1 項')).toBeVisible();
  });

  await runStep(5, 'continue to Section 3 and open gallery with expected marketing image count', async () => {
    await page.getByRole('button', { name: '繼續 → 選擇製圖方式' }).click();
    const section = page.locator('#dt-step-3');
    await expect(section).toHaveClass(/glow-active/);
    await section.getByRole('button', { name: /範例庫/ }).click();
    await expect(section.getByText(/\d+ 條符合 · 來源 CC BY 4\.0/)).toBeVisible();

    const count = await visibleGalleryCount(section);
    /* §A 加 evolink-ecommerce + evolink-poster 入 image sub 後，marketing+image 預期 40-60 條 */
    if (!(count > 30 && count <= 70)) {
      throw new Error(`Expected marketing/image gallery count > 30 and <= 70, got ${count}`);
    }
  });

  await runStep(6, 'verify gallery card metadata includes EvoLinkAI and wuyoscar categories', async () => {
    const section = page.locator('#dt-step-3');
    const metaTexts = await section.locator('.text-xs.text-slate-500').allTextContents();
    const hasEvoLink = metaTexts.some(text => /^EvoLinkAI · /.test(text.trim()));
    const hasWuyoscarCategory = metaTexts.some(text => /Typography|Photography|Product|Cinematic|Scientific|UI\/UX|Brand/i.test(text));
    const sample = metaTexts.map(text => text.trim()).filter(Boolean).slice(0, 6).join(' | ');
    if (!hasEvoLink || !hasWuyoscarCategory) {
      throw new Error(`Expected visible metadata from EvoLinkAI and wuyoscar categories, got hasEvoLink=${hasEvoLink}, hasWuyoscarCategory=${hasWuyoscarCategory}; sample=${sample}`);
    }
  });

  await runStep(7, 'switch to proto sub and verify filtered gallery remains non-empty', async () => {
    const section = page.locator('#dt-step-3');
    await section.getByRole('button', { name: /設計稿\/原型|UI 原型|原型/ }).click();
    await expect(section.getByText(/\d+ 條符合 · 來源 CC BY 4\.0/)).toBeVisible();

    const count = await visibleGalleryCount(section);
    expect(count).toBeGreaterThan(0);
  });

  await runStep(8, 'verify console errors', async () => {
    expect(errors, errors.join('\n')).toEqual([]);
  });

  const report = {
    totalSteps: 8,
    passed: stepStatus.filter(s => s.ok).length,
    failed: failures.length,
    consoleErrors: errors.length,
    failures,
    stepStatus,
    screenshots: Array.from({ length: 8 }, (_, i) => screenshotPath(i + 1)),
  };
  fs.writeFileSync('.playwright/sprint1.5A-verify-report.json', JSON.stringify(report, null, 2));

  console.log('\n## Playwright Sprint 1.5 §A 驗證結果');
  console.log(`- 總步驟: ${report.totalSteps}`);
  console.log(`- 通過: ${report.passed}`);
  console.log(`- 失敗: ${report.failed}`);
  console.log(`- console errors: ${report.consoleErrors}`);
  if (failures.length) {
    console.log('### 失敗清單');
    for (const f of failures) {
      console.log(`- Step ${String(f.step).padStart(2, '0')}: ${f.description} -> ${f.reason} (${f.screenshot})`);
    }
  }

  expect(failures, `Step failures:\n${failures.map(f => `Step ${String(f.step).padStart(2, '0')}: ${f.reason}`).join('\n')}`).toEqual([]);
  expect(errors, `Console errors:\n${errors.join('\n')}`).toEqual([]);
});
