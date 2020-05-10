# selenium-grid-file-download-workaround
Selenium provides possiblity to download files to local machine. However when using remote webdriver from local machine, in order to connect to remotely located selenium grid, the file download only downloads file to the remotely located grid machine. 

This is just a  workaround to download the file to the local machine. Workaround is simply that the selenium sessions cookies are read and copied to session created by requests and then performing the file download for the same file that was already downloaded to the remote grid. This code snippet includes only the reading and storing session cookies, file download (through requests) and saving file content parts.

## install required Python3 libraries
```
python3 -m pip install -r requirements.txt
```

## make a test run
```
python3 test.py
```

License
-------

selenium-grid-file-download-workaround is free and unencumbered public domain software. For more
information, see <http://unlicense.org/> or the accompanying UNLICENSE file.
