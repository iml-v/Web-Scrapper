import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import xlsxwriter
from datetime import date, timedelta
import threading
import time
import sys

class ParserThread(threading.Thread):
    def __init__(self, date, browser):
        threading.Thread.__init__(self)
        self.date = date
        self.browser = browser
        self.results = []
    def run(self):
        print('Scraping {}'.format(self.date))
        self.results = get_results(self.date, self.browser)
        print('Finished Scraping {}'.format(self.date))

class Result:
    def __init__(self, date, result):
        self.date = date
        self.result = result

def get_results(date, browser):

    date_string = '{}/{}/{}'.format(date.day,
        date.month, date.year)

    url = generate_url(date)
    raw_results = parse(url, browser)

    if raw_results is None:
        return None

    results = [Result(date_string, raw_result) for raw_result in raw_results]
    return results

def parse(url, browser):
    browser.get(url)

    try:
        WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'naps-list-contain'))
        )
    except TimeoutException:
        print('Timed out waiting for page to load')
        return None

    nap_row_elements = browser.find_elements_by_class_name('dog-list-item')
    raw_results = [nap_row_element.find_element_by_xpath('td[4]').text
                    for nap_row_element in nap_row_elements]

    return raw_results

def generate_url(date):
    date_array = date.strftime('%d %B %Y').split()
    day = date_array[0]
    month = date_array[1].lower()
    year = date_array[2]

    base_url = 'http://racing.betting-directory.com/'
    url = base_url + 'naps/{}th-{}-{}.php'.format(day, month, year)
    return url

def write_entries(worksheet, results):
    row = 1
    for result in results:
        worksheet.write(row, 0, result.date)
        worksheet.write(row, 1, result.result)
        row += 1

if __name__ == '__main__':

    # global variables
    workbook = xlsxwriter.Workbook('results.xlsx')
    start_date = date(2016, 12, 1)
    end_date = date(2016, 12, 12)
    num_browsers = 1

    worksheet = workbook.add_worksheet()

    # worksheet headers
    worksheet.write(0, 0, 'Date')
    worksheet.write(0, 1, 'Results')

    # selenium web driver settings
    chrome_path = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver_win32/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('-incognito')
    chrome_options.add_argument('--window-size=300,300')

    # initiate browsers
    browsers = [webdriver.Chrome(executable_path=chrome_path,
        chrome_options=chrome_options) for _ in range(num_browsers)]

    skipped_dates = []
    results = []
    current_date = start_date
    try:
        while current_date <= end_date:
            threads = []
            thread_count = 0
            while thread_count < num_browsers:
                t = ParserThread(current_date, browsers[thread_count])
                t.start()
                threads.append(t)
                thread_count += 1
                current_date += timedelta(days=1)
                if current_date > end_date:
                    break
                time.sleep(1)
            for t in threads:
                t.join()
            for t in threads:
                if t.results is not None:
                    results.extend(t.results)
                else:
                    skipped_dates.append(t.date)

    finally:
        # write data to file
        write_entries(worksheet, results)

        # cleanup
        for browser in browsers:
            browser.quit()
        workbook.close()
