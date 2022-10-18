import { test, expect } from '@playwright/test';
import * as fs from 'fs';

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

var logger = fs.createWriteStream('output/output.txt', {
    flags: 'a' // 'a' means appending (old data will be preserved)
})

test('test', async ({ page }) => {
    await page.goto('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent');
    // await page.goto('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent&Year=2022');
    delay(5000)
    var pastMeetingLocator = page.locator(".past-meetings")
    var accordians = pastMeetingLocator.getByRole('button', { expanded: false })
    var accordianCount = await accordians.count();
    console.log("accordianCount", accordianCount)
    for (let i = 0; i < accordianCount; i++) {
        // for (let i = 0; i < 3; i++) {
        console.log("i=", i)
        accordians.nth(i).click();
        await delay(20000)
    }

    var pastMeetingHtml = await pastMeetingLocator.innerHTML()
    logger.write(pastMeetingHtml);
});