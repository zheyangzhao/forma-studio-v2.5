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

test('Sprint 1.5 B - gallery 接 4 區塊 UI 11 步驗證', async ({ page }) => {
  fs.mkdirSync('.playwright', { recursive: true });

  const errors = [];
  const failures = [];
  const stepStatus = [];
  const screenshotPath = step => `.playwright/sprint1-verify-${String(step).padStart(2, '0')}.png`;

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

  await runStep(1, 'goto page and verify gallery globals', async () => {
    await page.goto('http://localhost:8765/forma-studio.html', { waitUntil: 'networkidle' });
    await expect(page).toHaveTitle(/Forma Studio/);
    const meta = await page.evaluate(() => ({
      total: window.FORMA_GALLERY?.total_count,
      enabled: window.ENABLE_PROMPT_GALLERY,
      lexicalTotal: typeof FORMA_GALLERY !== 'undefined' ? FORMA_GALLERY?.total_count : undefined,
      lexicalEnabled: typeof ENABLE_PROMPT_GALLERY !== 'undefined' ? ENABLE_PROMPT_GALLERY : undefined,
    }));
    expect(meta.total).toBe(66);
    expect(meta.enabled).toBe(true);
  });

  await runStep(2, 'find API key input and fill dummy key', async () => {
    await page.getByRole('button', { name: /設定 API Key|設定 OpenAI API Key|API Key 已設定/ }).first().click();
    const input = page.locator('input[placeholder="sk-proj-..."]').last();
    await expect(input).toBeVisible();
    await input.fill('sk-test-dummy-not-real');
    await expect(input).toHaveValue('sk-test-dummy-not-real');
    await snap(2);
    await page.getByRole('button', { name: '儲存' }).last().click();
  });

  await runStep(3, 'fill Section 1 requirement textarea', async () => {
    const textarea = page.locator('#dt-step-1 textarea').first();
    await expect(textarea).toBeVisible();
    await textarea.fill('我要做一份併購交易的提案書封面');
    await expect(textarea).toHaveValue('我要做一份併購交易的提案書封面');
  });

  await runStep(4, 'continue to Section 2', async () => {
    await page.getByRole('button', { name: '繼續 → 設定受眾與基調' }).click();
    await expect(page.locator('#dt-step-2')).toHaveClass(/glow-active/);
  });

  await runStep(5, 'select legal industry chip', async () => {
    const section = page.locator('#dt-step-2');
    const legalChip = section.getByRole('button', { name: /律師/ });
    await legalChip.click();
    await expect(legalChip).toHaveClass(/border-emerald-400/);
    await expect(section.getByText('1 項')).toBeVisible();
  });

  await runStep(6, 'continue to Section 3', async () => {
    await page.getByRole('button', { name: '繼續 → 選擇製圖方式' }).click();
    await expect(page.locator('#dt-step-3')).toHaveClass(/glow-active/);
  });

  await runStep(7, 'open gallery secondary controls', async () => {
    /* sub=image + industries=legal 預期命中 0 條（legal 不在 image 對應的 slug），驗證空狀態 fallback */
    const section = page.locator('#dt-step-3');
    await section.getByRole('button', { name: /範例庫/ }).click();
    await expect(section.getByText(/\d+ 條符合 · 來源 CC BY 4\.0/)).toBeVisible();
    await expect(section.getByText(/目前條件沒有符合的範例/)).toBeVisible();
  });

  await runStep(8, 'switch primary subTab to info and verify filtered gallery cards', async () => {
    const section = page.locator('#dt-step-3');
    await section.getByRole('button', { name: /資訊圖表/ }).click();
    await expect(section.getByText(/\d+ 條符合 · 來源 CC BY 4\.0/)).toBeVisible();
    const countText = await section.locator('span', { hasText: /條符合 · 來源 CC BY 4\.0/ }).textContent();
    const count = Number((countText || '').match(/(\d+)\s+條符合/)?.[1]);
    expect(count).toBeGreaterThanOrEqual(6);
    expect(count).toBeLessThanOrEqual(9);
    const firstCard = section.getByRole('button', { name: '套用' }).first().locator('xpath=ancestor::div[contains(@class, "rounded-xl") and contains(@class, "border-slate-700")][1]');
    await expect(firstCard.locator('.text-sm.font-bold')).toBeVisible();
    await expect(firstCard.locator('.text-xs.text-slate-500')).toContainText(/Infographics|Data Visualization|Technical Illustration|Scientific/i);
    await expect(firstCard.locator('.text-xs.text-slate-500')).toContainText(/portrait|landscape|wide|tall|square|size n\/a/i);
  });

  await runStep(9, 'apply first gallery prompt and verify image sub restore', async () => {
    const section = page.locator('#dt-step-3');
    const firstCard = section.getByRole('button', { name: '套用' }).first().locator('xpath=ancestor::div[contains(@class, "rounded-xl") and contains(@class, "border-slate-700")][1]');
    const preview = await firstCard.locator('p').textContent();
    await firstCard.getByRole('button', { name: '套用' }).click();
    await expect(section.getByRole('button', { name: /圖像生成/ })).toHaveClass(/sub-on/);
    await expect(section.getByRole('button', { name: /範例庫/ })).not.toHaveClass(/border-emerald-400/);
    const desc = section.locator('textarea').first();
    await expect(desc).toBeVisible();
    const descValue = await desc.inputValue();
    expect(descValue.length).toBeGreaterThan(80);
    expect(descValue).toContain((preview || '').replace('...', '').slice(0, 30));
  });

  await runStep(10, 'verify Section 4 exists', async () => {
    await expect(page.locator('#dt-step-4')).toBeVisible();
  });

  await runStep(11, 'click copy button and verify copied state', async () => {
    /* Step 9 後 showGallery=false + sub=image，無 OutBox 也無 CopyBtn；改：切 info sub + 重開範例庫 + 點第一張卡片的複製鈕 */
    const section = page.locator('#dt-step-3');
    await section.getByRole('button', { name: /資訊圖表/ }).click();
    await section.getByRole('button', { name: /範例庫/ }).click();
    const firstCard = section.getByRole('button', { name: '套用' }).first().locator('xpath=ancestor::div[contains(@class, "rounded-xl") and contains(@class, "border-slate-700")][1]');
    await expect(firstCard).toBeVisible();
    const copyButton = firstCard.getByRole('button', { name: /📋 複製/ });
    await copyButton.click();
    await expect(firstCard.getByRole('button', { name: /✅ 已複製/ })).toBeVisible();
  });

  const report = {
    totalSteps: 11,
    passed: stepStatus.filter(s => s.ok).length,
    failed: failures.length,
    consoleErrors: errors.length,
    failures,
    stepStatus,
    screenshots: Array.from({ length: 11 }, (_, i) => screenshotPath(i + 1)),
  };
  fs.writeFileSync('.playwright/sprint1-verify-report.json', JSON.stringify(report, null, 2));

  console.log('\n## Playwright 11 步驗證結果');
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
