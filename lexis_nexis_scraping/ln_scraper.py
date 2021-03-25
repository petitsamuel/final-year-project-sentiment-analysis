from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from shared.folders import download_folder
import os
import time
import numpy as np
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')
username = os.getenv('LN_USERNAME')
password = os.getenv('LN_PASSWORD')
path_to_chromedriver = os.getenv('CHROME_DRIVER')
dead_time = os.getenv('TIMEOUT')
page_size = os.getenv('PAGE_SIZE')

# Parse settings from .env file
if url == None or username == None or password == None or path_to_chromedriver == None or dead_time == None or page_size == None:
    print("Expected the following variables to be set from .env file: URL, LN_USERNAME, LN_PASSWORD, CHROME_DRIVER, TIMEOUT, PAGE_SIZE")
    exit(1)
try:
    dead_time = int(dead_time)
    page_size = int(page_size)
except:
    print("TIMEOUT and PAGE_SIZE must be int values")
    exit(1)


def wait_for_download_triggered():
    print("Waiting for download to trigger")
    start_time = int(time.time())
    while all([not filename.endswith(".crdownload") for filename in os.listdir(download_folder)]):
        if time.time() - start_time > dead_time:
            raise Exception({'error': 'delay expired'})
        # click on the loading window if present to trigger a status update
        if (int(time.time()) - start_time) % 15 == 0:
            try:
                browser.find_element_by_xpath(
                    '//*[@id="delivery-popin"]').click()
                print("Clicked the loading spinner")
            except:
                print("Couldn't find loading window")
        time.sleep(1)
    print("Download triggered!")


def wait_for_download_done():
    print("Waiting for download to complete")
    start_time = time.time()
    while any([filename.endswith(".crdownload") for filename in os.listdir(download_folder)]):
        if time.time() - start_time > dead_time:
            raise Exception({'error': 'delay expired'})
        time.sleep(2)
    print("File download finished!")


def rename_downloaded_file(page, total):
    print("Renaming file for indexing")
    try:
        files = [filename for filename in os.listdir(
            download_folder) if filename.startswith("Files ") or filename == "ZIP"]
        assert len(files) == 1
        os.rename(download_folder + "/" +
                  files[0], download_folder + '/%d_%d.zip' % (page, total))
        print("File renamed to %s" % ('%d_%d.zip' % (page, total)))
    except Exception as e:
        print(e)
        print("failed to rename file to be indexed")
        exit(1)


def clean_download_dir():
    print("Cleaning download directory...")
    for file in os.listdir(download_folder):
        if file.endswith(".crdownload") or file.startswith("Files ") or file == "ZIP":
            os.remove(os.path.join(download_folder, file))


# Return True if a downloaded file does not exist for current page
def should_download_page(page, total):
    return not any([filename == '%d_%d.zip' % (page, total)
                    for filename in os.listdir(download_folder)])


def wait_is_rendered_click(selector, click_xpath):
    # Wait for dialog to display
    dialog = None
    start_time = time.time()
    while not dialog:
        try:
            if time.time() - start_time > dead_time:
                raise Exception({'error': 'delay expired'})
            dialog = browser.find_element_by_xpath(selector)
            time.sleep(2)
            browser.find_element_by_xpath(click_xpath).click()
            break
        except:
            time.sleep(0.1)
            continue


def wait_is_rendered(selector):
    # Wait for dialog to display
    dialog = None
    start_time = time.time()
    while not dialog:
        try:
            if time.time() - start_time > dead_time:
                raise Exception({'error': 'delay expired'})
            dialog = browser.find_element_by_xpath(selector)
            break
        except:
            time.sleep(0.1)
            continue


# Get Page Info
total_number = 350904  # article count (found by hand)
total_page = int(np.ceil(total_number/page_size))

# Setup chrome driver
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_folder}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.headless = True
browser = webdriver.Chrome(
    executable_path=path_to_chromedriver, options=chromeOptions)
browser.set_window_size(1800, 1000)

# Login
print("Loading login page")
browser.get(url)
input_elements = browser.find_elements_by_id('entry')
input_elements[0].send_keys(username)
input_elements[1].send_keys(password)
input_elements[1].send_keys(Keys.ENTER)

try:
    # Accept dialog page
    time.sleep(1)
    print("Accepting redirect page")
    browser.find_element_by_xpath(
        '//*[@id="kv7k"]/div/div/div/section/div/menu/input[1]').click()
except:
    # If page is not shown - continue to search
    pass

# Uncomment below if an information dialog is shown (pendo titled)
# Wait for announcement dialog to display & close it
# wait_is_rendered_click('//*[@id="pendo-guide-container"]',
#                        '/html/body/div[3]/div/div/button')
# time.sleep(1)
# wait_is_rendered_click('//*[@id="pendo-guide-container"]',
#                        '/html/body/div[4]/div/div/button')
print("Starting download...")
for page in range(total_page):
    clean_download_dir()
    if not should_download_page(page, total_page):
        print("Page %d out of %d already downloaded, skipping" %
              (page, total_page))
        continue
    print("Downloading page %d out of %d" % (page, total_page))
    wait_is_rendered('//*[@id="content"]/header')

    # Click download button
    browser.find_element_by_xpath(
        '//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[3]/ul/li[3]/button').click()
    wait_is_rendered('//*[@id="SelectedRange"]')

    browser.find_element_by_xpath('//*[@id="SelectedRange"]').send_keys(
        "%d-%d" % (((page * page_size) + 1), ((page + 1) * page_size)))
    browser.find_element_by_xpath('//*[@id="Rtf"]').click()
    browser.find_element_by_xpath(
        '//*[@id="SeparateFiles"]').click()
    browser.find_element_by_xpath('//*[@id="FileName"]').clear()
    browser.find_element_by_xpath(
        '//*[@id="FileName"]').send_keys(str(page) + '_' + str(total_page))
    browser.find_element_by_xpath(
        '//*[@id="tab-FormattingOptions"]').click()
    time.sleep(0.5)
    if browser.find_element_by_xpath('//*[@id="EmbeddedReferences"]').get_attribute('checked') == 'true':
        browser.find_element_by_xpath(
            '//*[@id="EmbeddedReferences"]').click()

    # click download
    browser.find_element_by_xpath(
        '/html/body/aside/footer/div/button[1]').click()

    wait_for_download_triggered()
    wait_for_download_done()
    time.sleep(0.5)
    rename_downloaded_file(page, total_page)

    print('Finished page: ' + str(page) +
          ' out of ' + str(total_page), end="\n\n\n")

print("Finished downloading!")
