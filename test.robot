*** Settings ***
Library    SeleniumLibrary

Suite Teardown    Close All Browsers

*** Test Cases ***
Headless Chrome - Create Webdriver
  ${chrome_options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
#  Call Method  ${chrome_options}  add_argument  headless
#  Call Method  ${chrome_options}  add_argument  disable-gpu
  ${prefs}=  Create Dictionary  prompt_for_download=false  download.default_directory=/home/seluser/videos
  Call Method  ${chrome_options}  add_experimental_option  prefs  ${prefs}
  #Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=headlesschrome  remote_url=http://localhost:4444/wd/hub  options=${chrome_options}
  Open Browser  url=https://www.mozilla.org/en-US/foundation/documents  browser=headlesschrome  remote_url=http://192.168.99.100:32630/wd/hub  options=${chrome_options}
  Click Link  css=[href$='.pdf']
  Sleep  10s
  Capture Page Screenshot
  #Sleep  600s

