*** Settings ***
Library    SeleniumLibrary

Suite Teardown    Close All Browsers

*** Test Cases ***
Local Headless Chrome Browser - Create Webdriver and Download PDF
  ${chrome_options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
  Call Method  ${chrome_options}  add_argument  headless
  Call Method  ${chrome_options}  add_argument  disable-gpu
  ${prefs}=  Create Dictionary  prompt_for_download=false  download.default_directory=${CURDIR}
  Call Method  ${chrome_options}  add_experimental_option  prefs  ${prefs}

  Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=headlesschrome  options=${chrome_options}
  Click Link  css=[href$='.pdf']
  Sleep  2s  # Wait for download to finish
