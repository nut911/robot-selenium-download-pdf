from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.ui import WebDriverWait
import base64
import os
import time


def get_webdriver_instance():
    lib = BuiltIn().get_library_instance('SeleniumLibrary')
    return lib.driver


def get_file_content_chrome():
  driver = get_webdriver_instance()
  uri = driver.current_url
  save_to_filename = uri.rsplit("/", 1)[1]
  result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),
    t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),
    o=0,c=0;64>c;++c)i[c]=
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    .charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],
    a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];
    return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,
    a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],
    a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
  if type(result) == int :
    raise Exception("Request failed with status %s" % result)
  with open(save_to_filename, 'wb') as file:
    file.write(base64.b64decode(result))


def get_filenames_moz(driver):
  driver.command_executor._commands["SET_CONTEXT"] = (
      "POST", "/session/$sessionId/moz/context")
  driver.execute("SET_CONTEXT", {"context": "chrome"})
  return driver.execute_async_script("""
    var { Downloads } = Components.utils
    .import('resource://gre/modules/Downloads.jsm', {});
    Downloads.getList(Downloads.ALL)
      .then(list => list.getAll())
      .then(entries => entries.filter(e => e.succeeded).map(e => e.target.path))
      .then(arguments[0]);
    """)
  driver.execute("SET_CONTEXT", {"context": "content"})


def moz_save_last_downloaded_file_content():
  driver = get_webdriver_instance()
  files = WebDriverWait(driver, 20, 1).until(get_filenames_moz)
  driver.execute("SET_CONTEXT", {"context": "chrome"})
  result = driver.execute_async_script("""
    var { OS } = Cu.import("resource://gre/modules/osfile.jsm", {});
    OS.File.read(arguments[0]).then(function(data) {
      var base64 = Cc["@mozilla.org/scriptablebase64encoder;1"]
      .getService(Ci.nsIScriptableBase64Encoder);
      var stream = Cc['@mozilla.org/io/arraybuffer-input-stream;1']
      .createInstance(Ci.nsIArrayBufferInputStream);
      stream.setData(data.buffer, 0, data.length);
      return base64.encodeToString(stream, data.length);
    }).then(arguments[1]);
    """, files[0])
  driver.execute("SET_CONTEXT", {"context": "content"})
  with open(files[0], 'wb') as file:
    file.write(base64.b64decode(result))


def get_selenium_session_id():
  driver = get_webdriver_instance()
  return driver.session_id
