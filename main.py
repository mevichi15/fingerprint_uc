
from cProfile import Profile
import json
import os
from random import randint
import shutil
import sys
import tempfile
from typing import Optional
import zipfile
from undetected_chromedriver import Chrome

import undetected_chromedriver as uc
# import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from collectionObject import Collection
from driver.extensions.fingerprint.chromeFinger import Fingerprint
from profile_1 import ProfileGenerator

def get_driver(proxyServer: Optional[int], proxyPort: Optional[int], proxyUsername: Optional[str], proxyPassword: Optional[str]) -> Chrome:
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--window-position=000,000")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en")
    options.add_argument("--password-store=basic")

    profile = ProfileGenerator().make()
    collection = Collection(values=profile, proxyServer=proxyServer, 
                                proxyPort=proxyPort,
                                proxyUsername=proxyUsername, 
                                proxyPassword=proxyPassword)
    fingerprint = collection.fingerprintOptions()
    capabilitiesOptions = collection.capabilitiesOptions()
    AdditionalOptions = collection.chromeOptions()
    options.add_argument(
        f'--window-size={AdditionalOptions["screen-resolution"]}')

    #load proxy
    if proxyServer and not proxyServer == 0:
        proxy = (proxyServer, proxyPort, proxyUsername, proxyPassword)
        proxy_extension = ProxyExtension(*proxy)
        options.add_argument(f"--load-extension={proxy_extension.directory},{initFingerprint(fingerprint)}")
    else : 
        options.add_argument(f"--load-extension={initFingerprint(fingerprint)}")

    driver = uc.Chrome(suppress_welcome=True,version_main=103, options=options, use_subprocess=True, desired_capabilities = capabilitiesOptions)
    return driver

def initFingerprint(fingerprint):
        fingerprint = Fingerprint(fingerprint)
        extensionPath = fingerprint.makeExtension()
        return extensionPath

def set_viewport_size(driver):
    # working =>
    # window_size = driver.execute_script("""
    #     return [1920 - Math.floor(Math.random() * 300),
    #       1080 - Math.floor(Math.random() * 300)];
    #     """)
    window_size = driver.execute_script("""
        return [1437 - Math.floor(Math.random() * 10),
        1004 - Math.floor(Math.random() * 10)];
        """)
    driver.set_window_size(*window_size)


class ProxyExtension:
    
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "adobe_pdf_%s",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "76.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """

    def __init__(self, host, port, user, password):
        self._dir = os.path.normpath(tempfile.mkdtemp())
        manifest_json = self.manifest_json % (str(randint(10,9999)))
        manifest_file = os.path.join(self._dir, "manifest.json")
        with open(manifest_file, mode="w") as f:
            f.write(manifest_json)

        background_js = self.background_js % (host, port, user, password)
        background_file = os.path.join(self._dir, "background.js")
        with open(background_file, mode="w") as f:
            f.write(background_js)

    @property
    def directory(self):
        return self._dir

    def __del__(self):
        # shutil.rmtree(self._dir)
        pass





## To get it to work call get_driver it will return the chrome driver