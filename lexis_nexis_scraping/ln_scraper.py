from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import numpy as np
from dotenv import load_dotenv
import sys
from pathlib import Path


URLS = [
    # "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2feb37d77e-e2b2-4601-9610-52f56f9e2fe5%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f1eba0e35-20c8-4255-835e-a6d2d5ce993e%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2fecbfadba-e745-47ff-8873-20cb8a448446%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2fbef9bdc1-6500-411e-9571-7d29cc1db8ce%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2fe5198d37-cd0a-4d2b-90c1-b91586614898%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f961432e4-6838-4458-8c1e-a8644f7ca3a8%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f2b9411fa-6ea3-42f0-9af1-1828d558abbe%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f19983128-fa22-461c-8309-de968122537d%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2fc25b2afa-438a-413f-83d8-0180725c879e%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f3075144c-d412-42f5-b76f-3d98c06e6484%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f1ddfb48e-fc0b-4d5b-8ce2-5e5f666f3e49%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://login.elib.tcd.ie/login?qurl=https://advance.lexis.com%2fapi%2fpermalink%2f333ae439-cc93-4945-bb74-3eed5af5407c%2f%3fcontext%3d1519360%26identityprofileid%3d69Q2VF60797",
    "https://advance-lexis-com.elib.tcd.ie/api/permalink/3f74bb18-7090-468c-a482-d126bce69b48/?context=1519360&identityprofileid=69Q2VF60797",
    "https://advance-lexis-com.elib.tcd.ie/api/permalink/18bd82d6-0440-40b3-af60-83049b915a55/?context=1519360&identityprofileid=69Q2VF60797",
    "https://advance-lexis-com.elib.tcd.ie/api/permalink/88a229a5-c519-4e55-a78d-4d78389fae03/?context=1519360&identityprofileid=69Q2VF60797",
    "https://advance-lexis-com.elib.tcd.ie/api/permalink/3e86697b-e685-4e1f-a6ca-07724e677382/?context=1519360&identityprofileid=69Q2VF60797",
    "https://advance-lexis-com.elib.tcd.ie/api/permalink/d7a93b42-e983-47d9-afdc-3626cae8d93d/?context=1519360&identityprofileid=69Q2VF60797",
]
BATCH_IDS = [
    # 'FEB_2020',
    'MARCH_1_2020',
    'MARCH_2_2020',
    'APRIL_1_2020',
    'APRIL_2_2020',
    'MAY_2020',
    'JUNE_2020',
    'JULY_2020',
    'AUG_2020',
    'SEPT_2020',
    'OCT_2020',
    'NOV_2020',
    'DEC_2020',
    'JAN_2021',
    'FEB_2021',
    'MARCH_2021',
    'MARCH_2_2021'
]
COUNTS = [
    # 2855,
    12973,
    20208,
    29377,
    23169,
    21465,
    22270,
    23458,
    24676,
    26424,
    25191,
    25298,
    20151,
    20397,
    26552,
    22294,
    22811
]


# XPath selectors
HEADER_SELECTOR = '//*[@id="content"]/header'
PENGU_POPU_CONTAINER_SELECTOR = '//*[@id="pendo-guide-container"]//button'
PENDO_BACKDROP_SELECTOR = '//*[@id="pendo-backdrop"]//button'
LOADING_SPINNER_SELECTOR = '//*[@id="delivery-popin"]'


# Return True if one of the values is None
def has_none_values(values):
    return None in values


# Clicking the spinning icon triggers a status update call
def click_loading_spinner():
    try:
        browser.find_element_by_xpath(LOADING_SPINNER_SELECTOR).click()
        print("Clicked the loading spinner")
    except:
        print("Couldn't find loading window")


# Wait for a .crdownload file to be present within the download directory
def wait_for_download_triggered():
    print("Waiting for download to trigger")
    start_time = int(time.time())
    while all([not filename.endswith(".crdownload") for filename in os.listdir(download_folder)]):
        if time.time() - start_time > dead_time:
            raise Exception({'error': 'delay expired'})
        # click on the loading window if present to trigger a status update
        if (int(time.time()) - start_time) % 15 == 0:
            click_loading_spinner()
        time.sleep(0.8)
    print("Download triggered!")


# Download is considered finished when the download dir does not have .crdownload files
def wait_for_download_done():
    print("Waiting for download to complete")
    start_time = time.time()
    while any([filename.endswith(".crdownload") for filename in os.listdir(download_folder)]):
        if time.time() - start_time > dead_time:
            raise Exception({'error': 'delay expired'})
        time.sleep(2)
    print("File download finished!")


# Move file from default zip name to be in its indexed directory, renamed with the page offset
def rename_downloaded_file(page, total, batch_id):
    print("Renaming file for indexing")
    try:
        files = [filename for filename in os.listdir(
            download_folder) if filename.startswith("Files ") or filename == "ZIP"]
        assert len(files) == 1
        os.rename(download_folder + "/" +
                  files[0], output_folder + "/" + batch_id + '/%d_%d.zip' % (page + 1, total))
        print("File renamed to %s" % ('%d_%d.zip' % (page + 1, total)))
    except Exception as e:
        print(e)
        print("failed to rename file to be indexed")
        exit(1)


# Remove tmp files & unindexed files from download dir
def clean_download_dir():
    print("Cleaning download directory...")
    for file in os.listdir(download_folder):
        if file.endswith(".crdownload") or file.startswith("Files ") or file == "ZIP":
            os.remove(os.path.join(download_folder, file))


# Return True if a downloaded file does not exist for current page & batch id
def should_download_page(page, total, batch_id):
    return not any([filename == '%d_%d.zip' % (page, total)
                    for filename in os.listdir(output_folder + "/" + batch_id)])


# Wait for selector 1 to be rendered then click on the button (selected within the xpath provided)
def anti_pendo_popup(selector, render_wait_time=45):
    print("Waiting for Info Modal to display")
    dialog = None
    start_time = time.time()
    while not dialog:
        try:
            if time.time() - start_time > render_wait_time:
                print("Element %s not found after over %d seconds... Moving on." % (
                    selector, render_wait_time))
                break
            dialog = browser.find_element_by_xpath(selector)
            time.sleep(0.5)
            dialog.click()
            print("Clicked to close dialog")
            break
        except:
            time.sleep(0.1)
            continue


# Wait for item to be displayed
def wait_is_rendered(selector):
    dialog = None
    start_time = time.time()
    wait_render_time = 30
    while not dialog:
        if time.time() - start_time > wait_render_time:
            raise Exception({'error': 'render time delay expired'})
        try:
            dialog = browser.find_element_by_xpath(selector)
            break
        except:
            time.sleep(0.1)
            continue


# Load a new URL and login if necessary
def login_user(url):
    print("Loading login page")
    browser.get(url)
    print("Signing user in")
    try:
        input_elements = browser.find_elements_by_id('entry')
        input_elements[0].send_keys(username)
        input_elements[1].send_keys(password)
        input_elements[1].send_keys(Keys.ENTER)
        time.sleep(1)
    except:
        print("Login page not found - user is likely already logged in")
        pass


# TCD redirects from the login page to a limit reached page when limit is reached
# Sleep 40 minutes and let the script re-trigger
def check_tcd_limit_reached():
    tcd_limit_reached = False
    try:
        elem = browser.find_element_by_xpath('/html/body/p[2]')
        if elem.text == "TCD E-Resources Access":
            tcd_limit_reached = True
    except:
        pass

    if tcd_limit_reached:
        print("TCD Download limit was reached")
        print("Closing Browser and exiting")
        browser.close()
        time.sleep(40 * 60)  # sleep 40 mins
        exit(1)


# Permanent links with pre-set parameters usually make the url redirect to a confirmation
# page. Click continue
def accept_lexis_nexis_redirect():
    try:
        print("Accepting redirect page")
        browser.find_element_by_xpath(
            '//*[@id="kv7k"]/div/div/div/section/div/menu/input[1]').click()
    except:
        print("Redirect page not shown, moving on")
        # If page is not shown - continue to search
        pass


# Download and Index files for a provided batch
def scrape(batch_id, url, total_page, total_number):
    login_user(url)
    check_tcd_limit_reached()
    accept_lexis_nexis_redirect()

    # Wait for announcement dialog to display & close it
    anti_pendo_popup(PENGU_POPU_CONTAINER_SELECTOR)
    # Sometimes another popup is shown, attempt to click it but only wait 2 seconds
    anti_pendo_popup(PENGU_POPU_CONTAINER_SELECTOR, 1)
    # Third popup which occasionaly displays
    anti_pendo_popup(PENDO_BACKDROP_SELECTOR, 1)

    print("Starting download...")
    for page in range(total_page):
        clean_download_dir()
        if not should_download_page(page + 1, total_page, batch_id):
            print("Page %d out of %d already downloaded, skipping" %
                  (page + 1, total_page))
            continue

        print("Downloading page %d out of %d" % (page + 1, total_page))
        wait_is_rendered(HEADER_SELECTOR)

        # Click download button
        browser.find_element_by_xpath(
            '//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[3]/ul/li[3]/button').click()

        # Fill download form
        wait_is_rendered('//*[@id="SelectedRange"]')
        browser.find_element_by_xpath('//*[@id="SelectedRange"]').send_keys(
            "%d-%d" % (((page * page_size) + 1), min(total_number, ((page + 1) * page_size))))
        browser.find_element_by_xpath('//*[@id="Rtf"]').click()
        browser.find_element_by_xpath(
            '//*[@id="SeparateFiles"]').click()
        browser.find_element_by_xpath('//*[@id="FileName"]').clear()
        browser.find_element_by_xpath(
            '//*[@id="FileName"]').send_keys(str(page) + '_' + str(total_page))
        browser.find_element_by_xpath(
            '//*[@id="tab-FormattingOptions"]').click()

        time.sleep(0.2)

        if browser.find_element_by_xpath('//*[@id="EmbeddedReferences"]').get_attribute('checked') == 'true':
            browser.find_element_by_xpath(
                '//*[@id="EmbeddedReferences"]').click()

        # click download
        browser.find_element_by_xpath(
            '/html/body/aside/footer/div/button[1]').click()

        wait_for_download_triggered()
        wait_for_download_done()
        time.sleep(0.5)
        rename_downloaded_file(page, total_page, batch_id)

        print('Finished page: ' + str(page + 1) +
              ' out of ' + str(total_page), end="\n\n\n")


def check_env_vars():
    # Parse settings from .env file - check they are all set
    if has_none_values([username, password, output_folder, path_to_chromedriver, dead_time, page_size, download_folder]):
        print("Expected the following variables to be set from .env file: LN_USERNAME, LN_PASSWORD, CHROME_DRIVER, TIMEOUT, PAGE_SIZE")
        exit(1)


def init_download_and_out_dirs():
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    Path(download_folder).mkdir(parents=True, exist_ok=True)


def init_dirs(ids):
    for batch_id in ids:
        Path(output_folder + "/" + batch_id).mkdir(parents=True, exist_ok=True)


def batch_is_done(batch_id, total_page):
    files = [filename for filename in os.listdir(
        output_folder + "/" + batch_id) if filename.lower().endswith(".zip")]
    return len(files) == total_page


def iterate_batches():
    for i in range(len(BATCH_IDS)):
        batch_id = BATCH_IDS[i]
        total_number = COUNTS[i]
        url = URLS[i]
        total_page = int(np.ceil(total_number/page_size))
        print("Batch ID: %s" % (batch_id))
        if batch_is_done(batch_id, total_page):
            print("Batch already fully downloaded. Moving to the next.")
            continue
        scrape(batch_id, url, total_page, total_number)


# Loading .env variables
load_dotenv()

username = os.getenv('LN_USERNAME')
password = os.getenv('LN_PASSWORD')
path_to_chromedriver = os.getenv('CHROME_DRIVER')
dead_time = os.getenv('TIMEOUT')
page_size = int(os.getenv('PAGE_SIZE'))
download_folder = os.getenv('DOWNLOAD_FOLDER')
output_folder = os.getenv('OUTPUT_FOLDER')

try:
    dead_time = int(dead_time)
    page_size = int(page_size)
except:
    print("TIMEOUT and PAGE_SIZE must be positive int values")
    exit(1)

check_env_vars()

# Setup chrome driver
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_folder}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.headless = True
browser = webdriver.Chrome(
    executable_path=path_to_chromedriver, options=chromeOptions)
browser.set_window_size(1800, 1000)

init_download_and_out_dirs()
init_dirs(BATCH_IDS)
iterate_batches()

browser.close()
print("Finished downloading!")
