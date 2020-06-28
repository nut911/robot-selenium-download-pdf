*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    RequestsLibrary
Library    OperatingSystem
Library    helper.py

Suite Teardown    Close All Browsers

*** Test Cases ***
Remote Firefox Browser - Create Webdriver and Download PDF
  ${ff_capabilities}  Evaluate  sys.modules['selenium.webdriver'].common.desired_capabilities.DesiredCapabilities.FIREFOX  sys,selenium.webdriver
  ${ff_options}=  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys, selenium.webdriver
  Set To Dictionary  ${ff_capabilities}  testFileNameTemplate={proxyName}_{testName}_{browser}_{platform}_{testStatus}
  Call Method  ${ff_options}  set_capability  marionette  ${TRUE}
  Call Method  ${ff_options}  set_capability  acceptInsecureCerts  ${TRUE}
  Call Method  ${ff_options}  set_preference  browser.download.dir  /home/seluser/videos
  Call Method  ${ff_options}  set_preference  browser.helperApps.neverAsk.saveToDisk  application/octet-stream,application/pdf
  Call Method  ${ff_options}  set_preference  browser.download.useDownloadDir  ${TRUE}
  Call Method  ${ff_options}  set_preference  browser.download.manager.showWhenStarting  ${FALSE}
  Call Method  ${ff_options}  set_preference  browser.download.animateNotifications  ${FALSE}
  Call Method  ${ff_options}  set_preference  browser.safebrowsing.downloads.enabled  ${FALSE}
  Call Method  ${ff_options}  set_preference  browser.download.folderList  ${2}
  Call Method  ${ff_options}  set_preference  pdfjs.disabled  ${TRUE}

  Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=firefox  remote_url=http://192.168.99.100:32630/wd/hub  desired_capabilities=${ff_capabilities}  options=${ff_options}
  Click Link  css=[href$='.pdf']
  Add Cookie  zaleniumVideo  false  # toggle copying of /videos -folder contents
  Add Cookie  zaleniumVideo  true
  ${session_id}=  Get Selenium Session Id
  Create Session  pdf  http://192.168.99.100:32630
  ${resp}=  Get Request  pdf  /dashboard/zalenium_${session_id}_firefox_LINUX_COMPLETED.pdf  # here ${testName} is ${session_id} since testname was not set
  Status Should Be  200  ${resp}
  Create Binary File  ${EXECDIR}/zalenium_${session_id}_firefox_LINUX_COMPLETED.pdf  ${resp.content}
