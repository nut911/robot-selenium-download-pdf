*** Settings ***
Library    SeleniumLibrary
Library    helper.py

Suite Teardown    Close All Browsers

*** Test Cases ***
Local Chrome Browser - Create Webdriver and Download PDF
  ${chrome_options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
  ${prefs}=  Create Dictionary  prompt_for_download=false  download.default_directory=${CURDIR}
  Call Method  ${chrome_options}  add_experimental_option  prefs  ${prefs}

  Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=chrome  options=${chrome_options}
  Click Link  css=[href$='.pdf']
  Get File Content Chrome
