import { test, expect } from '@playwright/test';

test('judge can correct, refresh, request, approve and invalidate a revision', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/');
  await page.getByRole('button',{name:'Creator',exact:true}).click();
  await page.getByRole('button',{name:'Open workspace'}).click();
  await page.getByRole('button',{name:'New review',exact:true}).click();
  await page.getByLabel('Content title').fill('Judge browser journey');
  await page.getByLabel('Campaign purpose').fill('Announce Northstar One');
  await page.getByLabel('Draft text',{exact:true}).fill('Enjoy 20 hours of battery life.');
  await page.getByRole('button',{name:'Save revision'}).click();
  await page.getByRole('button',{name:'Run checks',exact:true}).click();
  await expect(page.getByText('Checks complete',{exact:true})).toBeVisible();
  await page.getByText('Accept or edit correction',{exact:true}).click();
  await page.getByRole('button',{name:'Preview exact change'}).click();
  await expect(page.getByText('Enjoy up to 12 hours of battery life.',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Accept and save new revision'}).click();
  await page.reload();
  await expect(page.getByRole('heading',{name:'Judge browser journey',exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Run checks',exact:true}).click();
  await page.getByRole('button',{name:'Request approval',exact:true}).click();
  await expect(page.locator('.page-head .badge')).toHaveText('awaiting review');
  await page.getByRole('button',{name:'Sign out'}).click();
  await page.getByRole('button',{name:'Reviewer',exact:true}).click();
  await page.getByRole('button',{name:'Open workspace'}).click();
  await page.getByText('Judge browser journey',{exact:true}).click();
  await page.getByLabel('Comment or decision reason').fill('Verified source and campaign intent.');
  await page.getByRole('button',{name:'Approve revision',exact:true}).click();
  await expect(page.locator('.page-head .badge')).toHaveText('approved');
  await page.screenshot({path:'test-results/approved-desktop.png',fullPage:true});
  await page.getByRole('button',{name:'Sign out'}).click();
  await page.getByRole('button',{name:'Creator',exact:true}).click();
  await page.getByRole('button',{name:'Open workspace'}).click();
  await page.getByText('Judge browser journey',{exact:true}).click();
  await page.getByRole('button',{name:'Edit revision',exact:true}).click();
  await page.getByLabel('Draft text',{exact:true}).fill('Meet Northstar One.');
  await page.getByRole('button',{name:'Save revision'}).click();
  await expect(page.locator('.page-head .badge')).toHaveText('draft');
  expect(errors).toEqual([]);
});

test('mobile login fits and has labelled keyboard-operable inputs',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 await expect(page.getByLabel('Email',{exact:true})).toBeVisible();
 await expect(page.getByLabel('Password',{exact:true})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy();
 await page.screenshot({path:'test-results/login-mobile.png',fullPage:true});
});
