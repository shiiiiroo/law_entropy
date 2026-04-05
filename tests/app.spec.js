import { test, expect } from '@playwright/test';

test.describe('Law Entropy App', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
    // Ensure the page is ready
    await page.waitForSelector('.app');
  });

  test('should load the page correctly', async ({ page }) => {
    await expect(page).toHaveTitle(/Law Entropy/);
    await expect(page.locator('.brand-logo')).toContainText('Law Entropy');
  });

  test('should load demo data and show stats with entropy index', async ({ page }) => {
    // Click demo button
    const demoBtn = page.locator('.demo-btn');
    await demoBtn.click();
    
    // Stats should appear
    const stats = page.locator('#stats');
    await expect(stats).toBeVisible();
    
    // Entropy index should be present
    const entropyStat = page.locator('#st-e');
    await expect(entropyStat).toBeVisible();
    
    // Check if documents are listed
    const docItems = page.locator('.doc-row');
    await expect(docItems).toHaveCount(3);
  });

  test('should run mock analysis and update entropy', async ({ page }) => {
    await page.locator('.demo-btn').click();
    
    // Run analysis
    await page.locator('#run-btn').click();
    
    // Check if results appear
    const resultCards = page.locator('.rcard');
    await expect(resultCards.first()).toBeVisible({ timeout: 15000 });

    // Entropy should be calculated (not 0% or empty)
    const entropyText = await page.locator('#st-e').innerText();
    expect(entropyText).not.toBe('0');
    expect(entropyText).toContain('%');
  });

  test('should switch panels and clear chat', async ({ page }) => {
    // Go to chat
    await page.locator('#nav-chat').click();
    await expect(page.locator('#panel-chat')).toHaveClass(/active/);

    // Type something
    await page.locator('#cinput').fill('Test message');
    await page.keyboard.press('Enter');

    // Message should appear
    await expect(page.locator('.cmsg.user')).toBeVisible();

    // Clear chat
    await page.locator('#clear-chat-btn').click();
    
    // User message should be gone
    await expect(page.locator('.cmsg.user')).toHaveCount(0);
  });
});
