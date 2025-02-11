import { test } from '@playwright/test';
import * as fs from 'fs';

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

test('test', async ({ page }) => {
    // full history
    // await page.goto('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent');

    // just for 2025
    await page.goto('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent&Year=2025');
    
    delay(5000)
    var pastMeetingLocator = page.locator(".past-meetings")
    var accordians = pastMeetingLocator.getByRole('button', { expanded: false })
    var accordianCount = await accordians.count();
    console.log("accordianCount", accordianCount)
    for (let i = 0; i < accordianCount - 1; i++) {
        console.log("i=", i)
        var accordian = accordians.nth(i)
        await accordian.click({ "trial": true })
        accordians.nth(i).click();
        await delay(20000)
        var logger = fs.createWriteStream('../playwright-output/output.txt', {
            flags: 'w' // 'a' means appending (old data will be preserved)
        })
        // write and overwrite the file so we don't lose all data if the scraper crashes
        var pastMeetingHtml = await pastMeetingLocator.innerHTML()
        logger.write(pastMeetingHtml);
    }
});