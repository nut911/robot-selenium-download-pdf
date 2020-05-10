import requests
from selenium import webdriver

# open browser to url
browser = webdriver.Chrome()
browser.get('http://ipv4.download.thinkbroadband.com')

# make requests - session
session = requests.Session()

# get cookies from existing selenium session
cookies = browser.get_cookies()

# set cookies for the requests session, i.e. local session
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# download file over the requests session
response = session.get('http://ipv4.download.thinkbroadband.com/5MB.zip')

# write bytes to file on disk
with open('test.zip', 'wb') as fp:
     fp.write(response.content)

# close response
response.close()

# close selenium session
browser.close()
session.close()
