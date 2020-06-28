*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    RequestsLibrary
Library    OperatingSystem
Library    helper.py

Suite Teardown    Close All Browsers

*** Test Cases ***
Remote Headless Chrome Browser - Create Webdriver and Download PDF
  ${chrome_options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
  Call Method  ${chrome_options}  add_argument  headless
  Call Method  ${chrome_options}  add_argument  disable-gpu
  ${prefs}=  Create Dictionary  prompt_for_download=false  download.default_directory=/home/seluser/videos
  Call Method  ${chrome_options}  add_experimental_option  prefs  ${prefs}
  ${capabilities}=  Create Dictionary  testFileNameTemplate={proxyName}_{testName}_{browser}_{platform}_{testStatus}

  Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=headlesschrome  remote_url=http://192.168.99.100:32630/wd/hub  options=${chrome_options}  desired_capabilities=${capabilities}
  Click Link  css=[href$='.pdf']
  Add Cookie  zaleniumVideo  false  # toggle copying of /videos -folder contents
  Add Cookie  zaleniumVideo  true
  ${session_id}=  Get Selenium Session Id
  Create Session  pdf  http://192.168.99.100:32630
  ${resp}=  Get Request  pdf  /dashboard/zalenium_${session_id}_chrome_LINUX_COMPLETED.pdf  # here ${testName} is ${session_id} since testname was not set
  Status Should Be  200  ${resp}
  Create Binary File  ${EXECDIR}/zalenium_${session_id}_chrome_LINUX_COMPLETED.pdf  ${resp.content}
