*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    helper.py

Suite Teardown    Close All Browsers

*** Test Cases ***
Local Firefox Browser - Create Webdriver and Download PDF
  ${ff_capabilities}  Evaluate  sys.modules['selenium.webdriver'].common.desired_capabilities.DesiredCapabilities.FIREFOX  sys,selenium.webdriver
  ${ff_options}=  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys, selenium.webdriver
  Call Method  ${ff_options}  set_capability  marionette  ${TRUE}
  Call Method  ${ff_options}  set_capability  acceptInsecureCerts  ${TRUE}
  Call Method  ${ff_options}  set_preference  browser.download.dir  ${CURDIR}
  Call Method  ${ff_options}  set_preference  browser.helperApps.neverAsk.saveToDisk  application/octet-stream,application/pdf
  Call Method  ${ff_options}  set_preference  browser.download.useDownloadDir  ${TRUE}
  Call Method  ${ff_options}  set_preference  browser.download.manager.showWhenStarting  ${FALSE}
  Call Method  ${ff_options}  set_preference  browser.download.animateNotifications  ${FALSE}
  Call Method  ${ff_options}  set_preference  browser.safebrowsing.downloads.enabled  ${FALSE}
  Call Method  ${ff_options}  set_preference  browser.download.folderList  ${2}
  Call Method  ${ff_options}  set_preference  pdfjs.disabled  ${TRUE}

  Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=firefox  desired_capabilities=${ff_capabilities}  options=${ff_options}
  Click Link  css=[href$='.pdf']
  Moz Save Last Downloaded File Content
