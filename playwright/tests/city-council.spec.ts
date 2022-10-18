import { test, expect } from '@playwright/test';
import * as fs from 'fs';

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

var logger = fs.createWriteStream('../output/output.txt', {
    flags: 'a' // 'a' means appending (old data will be preserved)
})

test('test', async ({ page }) => {

    // await page.goto('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent');
    await page.goto('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent&Year=2022');
    // var arrayElements = await page.$$(".PastMeetingTypesName")
    // console.log(arrayElements)
    delay(5000)
    var pastMeetingLocator = page.locator(".past-meetings")
    var accordians = pastMeetingLocator.getByRole('button', { expanded: false })
    var accordianCount = await accordians.count();
    for (let i = 0; i < accordianCount; i++) {
        var _locator = accordians.nth(i);
        await _locator.click();
        await delay(10000)
        var allCalendarItems = page.locator(".calendar-item")
        var calendarItemsCount = await allCalendarItems.count()
        expect(calendarItemsCount).toBeGreaterThan(0)
        for (let i = 0; i < calendarItemsCount; i++) {
            logger.write(allCalendarItems.nth(i).innerHTML());
        }
        // await expect(_locator).toHaveAttribute("aria-expanded", "true")
        // capture the inner html
        // console.log(_locator.innerHTML())
    }
    // arrayElements[0].click();
    // await page.getByRole('button', { name: ' Accessibility Advisory Committee Meeting (86 )' }).click();
    // delay(5000)
    // await expect(page).toHaveURL('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent&Expanded=Accessibility%20Advisory%20Committee%20Meeting');
    // await page.getByRole('button', { name: ' Accessibility Advisory Committee Meeting (86 )' }).click();
    // await expect(page).toHaveURL('https://pub-peterborough.escribemeetings.com/meetingscalendarview.aspx?FillWidth=1&wmode=transparent');

    // arrayElements[0].click();

});