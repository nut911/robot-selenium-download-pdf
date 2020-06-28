# selenium .pdf file download (no blob)
Selenium provides possiblity to download files to local machine. However when using remote webdriver from local machine, in order to connect to remotely located selenium grid, the file download only downloads file to the remotely located grid machine. 

The examples work by downloading the .pdf file to the local directory.
Examples work in following setups:
  - Local (host PC - server)
    - Chrome and Headless Chrome
    - Firefox and Headless Firefox
  - Remote (host PC - zalenium[selenium-grid] - server)
    - Chrome and Headless Chrome
    - Firefox and Headless Firefox

## install required Python3 libraries
```
python3 -m pip install -r requirements.txt
```

## make a test run
```
rm *.pdf ; robot local_chrome_pdf_no_blob.robot ; ls *.pdf
```


License
-------

selenium-grid-file-download-workaround is free and unencumbered public domain software. For more
information, see <http://unlicense.org/> or the accompanying UNLICENSE file.
