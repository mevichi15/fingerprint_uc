import json
import os
from random import randint
import tempfile
import undetected_chromedriver.v2 as webdriver
from functools import reduce
from services.utils.toolbox.driver.extensions.fingerprint.chromeFinger import Fingerprint
from services.utils.toolbox.driver.extensions.pointer.makePointer import makePointer
class ProxyExtension:
    
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "dkmkldskfmlksdf_%s",
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
    
class Session:
    def __init__(self, settings, capabilities, fingerprint):
        """
        Конструктор принимает набор парамметров для настрйки сессии
        шаблоны хранятся в chromeSettings

        :type fingerprint: dict
        :type capabilities: dict
        :type settings: dict
        """
        self.settings = settings
        self.capabilities = capabilities
        self.fingerprint = fingerprint

    def initFingerprint(self):
        """
        Создание объекта расширения для внедрения настроект отпечатка
        в браузер

        :return extensionPath: object
        """
        fingerprint = Fingerprint(self.fingerprint)
        extensionPath = fingerprint.makeExtension()
        return extensionPath

    def _chromeOptions(self,proxyServer, proxyPort, proxyUsername, proxyPassword) -> object:
        """
        Создание объекта настроект для сессии браузер
        - отключение webdriver = true
        - изменение разрешения экрана
        - установка значения user-agent
        - отключение WebRTC
        - инитиализация Fingerprint extension

        :return chromeOptionsDriver: object
        """
        chromeOptionsDriver = webdriver.ChromeOptions()
        # chromeOptionsDriver.add_experimental_option("debuggerAddress", debugger_address)
        chromeOptionsDriver.add_argument("--disable-dev-shm-usage")
        chromeOptionsDriver.add_argument("--no-sandbox")
        chromeOptionsDriver.add_argument("--disable-web-security")
        chromeOptionsDriver.add_argument("--disable-setuid-sandbox")
        chromeOptionsDriver.add_argument("--disable-accelerated-2d-canvas")
        chromeOptionsDriver.add_argument("--no-first-run")
        chromeOptionsDriver.add_argument("--disable-gpu")


        if self.settings['screen-resolution'] is not None:
            chromeOptionsDriver.add_argument(
                f'--window-size={self.settings["screen-resolution"]}')

        if self.settings['user-agent'] is not None:
            chromeOptionsDriver.add_argument(
                f'--user-agent={self.settings["user-agent"]}')
        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        chromeOptionsDriver.add_experimental_option("prefs", preferences)
        #schromeOptionsDriver.add_argument('--proxy-server=109.95.51.103:12231')
        # chromeOptionsDriver.add_argument(
        #     f'--user-data-dir=profiles/{self.settings["profile"]}')
        
        # chromeOptionsDriver.add_argument(f"--load-extension={self.initFingerprint()}")
        
        os.environ["LANGUAGE"] = "en" 
        chromeOptionsDriver.add_argument(f"--lang={os.getenv('LANGUAGE')}")
        if proxyServer and not proxyServer == 0:
            proxy = (proxyServer, proxyPort, proxyUsername, proxyPassword)
            proxy_extension = ProxyExtension(*proxy)
            # chromeOptionsDriver.add_argument(f"--load-extension={proxy_extension.directory},{makePointer()},{self.initFingerprint()}")
            chromeOptionsDriver.add_argument(f"--load-extension={proxy_extension.directory},{makePointer()},{self.initFingerprint()}")
        # chromeOptionsDriver.add_argument(f"--load-extension={makePointer()}")
        return chromeOptionsDriver

    def make(self, proxyServer, proxyPort, proxyUsername, proxyPassword) -> object:
        """
        Создание сесси с набором настроект
        возвращает объекта сесси для дальнейшего взаимодействия

        :return objectChrome: object
        """

        # objectChrome = webdriver.Remote(
        #     command_executor="http://localhost:4444/wd/hub",
        #     options=self._chromeOptions(),
        #     desired_capabilities=self.capabilities)
        # driver = uc.Chrome(version_main=102, desired_capabilities = self.capabilities, options=self._chromeOptions(), use_subprocess=True)
        # gl = GoLogin({
        # "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MmNiZmQ2MDQ0NDllYWE1YTllNDQ4NmQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MmNiZmUxZTMzMjE0ZTJlYjllYzFkMWUifQ.CAu56bZCEWfjrk756NF9Q_g2SRknj5lO3zmjA_Dj6eo",
        # "profile_id": "62cbfd604449ea34e9e4486f",
        # })
        # debugger_address = gl.start()
        driver = ChromeWithPrefs(suppress_welcome=True, version_main=102, options=self._chromeOptions(proxyServer, proxyPort, proxyUsername, proxyPassword), desired_capabilities = self.capabilities, use_subprocess=True)
        return driver


class ChromeWithPrefs(webdriver.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create an user_data_dir and add its path to the options
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]
