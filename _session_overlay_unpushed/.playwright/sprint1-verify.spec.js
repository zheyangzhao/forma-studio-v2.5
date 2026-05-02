  await runStep(7, 'open gallery secondary controls', async () => {
    /* sub=image + industries=legal 預期命中 0 條（legal 不在 image 對應的 slug），驗證空狀態 fallback */
    const section = page.locator('#dt-step-3');
    await section.getByRole('button', { name: /範例庫/ }).click();
    await expect(section.getByText(/\d+ 條符合 · 來源 CC BY 4\.0/)).toBeVisible();
    await expect(section.getByText(/目前條件沒有符合的範例/)).toBeVisible();
  });