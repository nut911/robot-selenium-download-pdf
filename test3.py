from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os, time, base64


def get_downloaded_files(driver):

  if not driver.current_url.startswith("chrome://downloads"):
    driver.get("chrome://downloads/")

  return driver.execute_script( \
     "return  document.querySelector('downloads-manager')  "
     " .shadowRoot.querySelector('#downloadsList')         "
     " .items.filter(e => e.state === 'COMPLETE')          "
     " .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url); ")

def get_file_content(driver, path):

  elem = driver.execute_script( \
    "var input = window.document.createElement('INPUT'); "
    "input.setAttribute('type', 'file'); "
    "input.hidden = true; "
    "input.onchange = function (e) { e.stopPropagation() }; "
    "return window.document.documentElement.appendChild(input); " )

  elem._execute('sendKeysToElement', {'value': [ path ], 'text': path})

  result = driver.execute_async_script( \
    "var input = arguments[0], callback = arguments[1]; "
    "var reader = new FileReader(); "
    "reader.onload = function (ev) { callback(reader.result) }; "
    "reader.onerror = function (ex) { callback(ex.message) }; "
    "reader.readAsDataURL(input.files[0]); "
    "input.remove(); "
    , elem)

  if not result.startswith('data:') :
    raise Exception("Failed to get file content: %s" % result)

  return base64.b64decode(result[result.find('base64,') + 7:])



capabilities_chrome = { \
    'browserName': 'chrome',
    'goog:chromeOptions': { \
      'args': [
      ],
      'prefs': { \
        # 'download.default_directory': "",
        # 'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        'plugins.always_open_pdf_externally': True,
        'safebrowsing_for_trusted_sources_enabled': False
      }
    }
  }

driver = webdriver.Chrome(desired_capabilities=capabilities_chrome)

# download a pdf file
driver.get("https://www.mozilla.org/en-US/foundation/documents")
driver.find_element_by_css_selector("[href$='.pdf']").click()

# list all the completed remote files (waits for at least one)
files = WebDriverWait(driver, 20, 1).until(get_downloaded_files)

# get the content of the first file remotely
content = get_file_content(driver, files[0])

# save the content in a local file in the working directory
with open(os.path.basename(files[0]), 'wb') as f:
  f.write(content)
