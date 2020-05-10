from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os, time, base64

def get_file_names_moz(driver):
  driver.command_executor._commands["SET_CONTEXT"] = ("POST", "/session/$sessionId/moz/context")
  driver.execute("SET_CONTEXT", {"context": "chrome"})
  return driver.execute_async_script("""
    var { Downloads } = Components.utils.import('resource://gre/modules/Downloads.jsm', {});
    Downloads.getList(Downloads.ALL)
      .then(list => list.getAll())
      .then(entries => entries.filter(e => e.succeeded).map(e => e.target.path))
      .then(arguments[0]);
    """)
  driver.execute("SET_CONTEXT", {"context": "content"})

def get_file_content_moz(driver, path):
  driver.execute("SET_CONTEXT", {"context": "chrome"})
  result = driver.execute_async_script("""
    var { OS } = Cu.import("resource://gre/modules/osfile.jsm", {});
    OS.File.read(arguments[0]).then(function(data) {
      var base64 = Cc["@mozilla.org/scriptablebase64encoder;1"].getService(Ci.nsIScriptableBase64Encoder);
      var stream = Cc['@mozilla.org/io/arraybuffer-input-stream;1'].createInstance(Ci.nsIArrayBufferInputStream);
      stream.setData(data.buffer, 0, data.length);
      return base64.encodeToString(stream, data.length);
    }).then(arguments[1]);
    """, path)
  driver.execute("SET_CONTEXT", {"context": "content"})
  return base64.b64decode(result)

capabilities_moz = { \
    'browserName': 'firefox',
    'marionette': True,
    'acceptInsecureCerts': True,
    'moz:firefoxOptions': { \
      'args': [],
      'prefs': {
        'browser.download.dir': '',
        'browser.helperApps.neverAsk.saveToDisk': 'application/octet-stream,application/pdf', 
        'browser.download.useDownloadDir': True, 
        'browser.download.manager.showWhenStarting': False, 
        'browser.download.animateNotifications': False, 
        'browser.safebrowsing.downloads.enabled': False, 
        'browser.download.folderList': 2,
        'pdfjs.disabled': True
      }
    }
  }

# launch Firefox
driver = webdriver.Firefox(capabilities=capabilities_moz)
#driver = webdriver.Remote('http://127.0.0.1:5555/wd/hub', capabilities_moz)

# download a pdf file
driver.get("https://www.mozilla.org/en-US/foundation/documents")
driver.find_element_by_css_selector("[href$='.pdf']").click()

# list all the downloaded files (waits for at least one)
files = WebDriverWait(driver, 20, 1).until(get_file_names_moz)

# get the content of the last downloaded file
content = get_file_content_moz(driver, files[0])

# save the content in a local file in the working directory
with open(os.path.basename(files[0]), 'wb') as f:
  f.write(content)

driver.close()

