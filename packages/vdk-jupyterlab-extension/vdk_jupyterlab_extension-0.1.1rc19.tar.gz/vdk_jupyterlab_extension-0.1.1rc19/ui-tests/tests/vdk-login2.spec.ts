/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

import { expect, test } from '@jupyterlab/galata';

/**
 * Don't load JupyterLab webpage before running the tests.
 * This is required to ensure we capture all log messages.
 */
test.use({ autoGoto: false });

test('should open run job pop up and then cancel the operation', async ({
  page
}) => {
  await page.goto('');
  await page.menu.open('VDK');
  await page.locator('#jp-vdk-menu').getByText('Login').click();
  await page.getByRole('button', { name: 'Click here to start.' }).click();
});