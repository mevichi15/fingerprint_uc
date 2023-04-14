import os
import tempfile
import zipfile
from pathlib import Path
from driver.extensions.fingerprint.data.canvas import canvasSerialization
from driver.extensions.fingerprint.data.platform import platformSerialization
from driver.extensions.fingerprint.data.webGL import webGLSerialization


class Fingerprint:
    __base_dir = Path(__file__).resolve().parent.parent
    __extensionPath = f'{__base_dir}/release/Fingerprint.zip'

    def __init__(self, fingerprint):
        self._fingerprint = fingerprint

    def __loadManifest(self):
        with open(f'{self.__base_dir}/fingerprint/data/manifest.json', "r") as file:
            manifest_json = file.read()
        manifest_json = manifest_json
        return manifest_json

    def __loadPlatform(self):
        return platformSerialization(self._fingerprint['platform'],
                                     self._fingerprint['deviceMemory'],
                                     self._fingerprint['hardwareConcurrency'])

    def __loadWebGL(self):
        return webGLSerialization(self._fingerprint['webGLHash'],
                                  self._fingerprint['webGLVendor'])

    def __loadCanvas(self):
        CanvasHash = dict(self._fingerprint['CanvasHash'])
        return canvasSerialization(CanvasHash)

    def makeExtension(self):
        extension_dir = os.path.normpath(tempfile.mkdtemp())

        manifestjson = self.__loadManifest()
        platformjs = self.__loadPlatform()
        webGL = self.__loadWebGL()
        canvas = self.__loadCanvas()


        manifest_file = os.path.join(extension_dir, "manifest.json")
        with open(manifest_file, mode="w") as f:
            f.write(manifestjson)

        platform_file = os.path.join(extension_dir, "platform.js")
        with open(platform_file, mode="w") as f:
            f.write(platformjs)

        webGL_file = os.path.join(extension_dir, "webGL.js")
        with open(webGL_file, mode="w") as f:
            f.write(webGL)

        canvas_file = os.path.join(extension_dir, "canvas.js")
        with open(canvas_file, mode="w") as f:
            f.write(canvas)

        return extension_dir

