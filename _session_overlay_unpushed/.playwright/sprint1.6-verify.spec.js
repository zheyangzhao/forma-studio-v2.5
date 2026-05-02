/* Sprint 1.5 §四 Tier 1.6 — Claude AI 一鍵增強鈕 Playwright 驗證 */
let test, expect;
try { ({ test, expect } = require('@playwright/test')); }
catch (e) { ({ test, expect } = require('playwright/test')); }
const fs = require('fs');

test.use({
  headless: true,
  viewport: { width: 1280, height: 900 },
  actionTimeout: 8000,
  permissions: ['clipboard-read', 'clipboard-write'],
});

test('Tier 1.6 — AI 增強鈕驗證（PLAN §4.3 fallback matrix）', async ({ page }) => {
  fs.mkdirSync('.playwright', { recursive: true });
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(`pageerror: ${err.message}`));

  const screenshotPath = step => `.playwright/sprint1.6-verify-${String(step).padStart(2,'0')}.png`;

  /* Step 1：載入 + 驗證 flag */
  await page.goto('http://localhost:8765/forma-studio.html', { waitUntil: 'networkidle' });
  const meta = await page.evaluate(() => ({
    enhanceFlag: window.ENABLE_AI_ENHANCE,
    galleryFlag: window.ENABLE_PROMPT_GALLERY,
    galleryTotal: window.FORMA_GALLERY?.total_count,
  }));
  expect(meta.enhanceFlag).toBe(true);
  expect(meta.galleryTotal).toBe(116);
  await page.screenshot({ path: screenshotPath(1), fullPage: true });

  /* Step 2：沒有 prompt output → 找不到 EnhanceBtn */
  await expect(page.getByRole('button', { name: /AI 增強/ })).toHaveCount(0);
  await page.screenshot({ path: screenshotPath(2), fullPage: true });

  /* Step 3：填描述 → 切到 Section 2 advisor mode → 生成 advisorOut */
  await page.locator('#dt-step-1 textarea').first().fill('我要做一份併購交易的提案書封面，受眾為企業 C-level');
  await page.getByRole('button', { name: '繼續 → 設定受眾與基調' }).click();
  await page.getByRole('button', { name: /🎨 方向顧問/ }).click();
  await page.getByRole('button', { name: /生成設計方向顧問 Prompt/ }).click();
  /* advisorOut 是純前端構造，不需要 API key */
  await expect(page.getByText('🎨 設計方向顧問 Prompt')).toBeVisible({ timeout: 5000 });
  await page.screenshot({ path: screenshotPath(3), fullPage: true });

  /* Step 4：EnhanceBtn 出現在 advisorOut 的 OutBox */
  const enhanceBtn = page.getByRole('button', { name: /AI 增強/ }).first();
  await expect(enhanceBtn).toBeVisible();
  await page.screenshot({ path: screenshotPath(4), fullPage: true });

  /* Step 5：沒填 API key → EnhanceBtn disabled */
  await expect(enhanceBtn).toBeDisabled();

  /* Step 6：填 dummy key（session only） */
  await page.getByRole('button', { name: /設定 API Key|API Key 已設定/ }).first().click();
  const keyInput = page.locator('input[placeholder="sk-proj-..."]').last();
  await keyInput.fill('sk-fake-not-real-key');
  await page.getByRole('button', { name: '儲存' }).last().click();

  /* Step 7：EnhanceBtn 變 enabled */
  await expect(enhanceBtn).toBeEnabled();
  await page.screenshot({ path: screenshotPath(7), fullPage: true });

  /* Step 8：點 EnhanceBtn → 假 key 會 401 → 3 秒內顯示 ⚠️ 失敗 → 原 prompt 不變 */
  const promptBox = page.locator('.font-mono.whitespace-pre-wrap').first();
  const oldText = await promptBox.textContent();
  expect(oldText.length).toBeGreaterThan(50);

  await enhanceBtn.click();
  /* 等到「增強中...」結束或錯誤訊息出現 */
  await expect(page.getByRole('button', { name: /增強失敗|回應為空/ })).toBeVisible({ timeout: 15000 });
  const newText = await promptBox.textContent();
  expect(newText).toBe(oldText);  /* 原 prompt 不能被破壞 */
  await page.screenshot({ path: screenshotPath(8), fullPage: true });

  /* Step 9：排除假 key 引發的 expected 網路 / CORS error，只檢查程式拋的 error */
  /* fake key 會觸發瀏覽器 fetch error / CORS error / 401 — 這是測試環境副作用。
     實際生產用真 key 不會有 CORS。
     這裡只 fail 在「程式內部拋的 error」（如 React render error / 未預期的 throw）。 */
  const programErrors = errors.filter(e =>
    !e.includes('Failed to load resource') &&
    !e.includes('net::ERR_FAILED') &&
    !e.includes('Access to fetch') &&
    !e.includes('CORS policy') &&
    !e.includes('Access-Control-Allow-Origin') &&
    !e.includes('the server responded with a status of 401') &&
    !e.includes('the server responded with a status of 4')
  );
  expect(programErrors, `Program errors:\n${programErrors.join('\n')}`).toEqual([]);
});
