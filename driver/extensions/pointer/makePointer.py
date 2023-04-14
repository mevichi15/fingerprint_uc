import os
import tempfile
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def manifestTransformation() -> str:
    manifest_json_file = open(str(BASE_DIR) + '/pointer/data/manifest.json')
    manifest_code = manifest_json_file.read()
    manifest_json_file.close()
    return manifest_code


def pointerTransformation() -> str:
    pointer_js_file = open(str(BASE_DIR) + '/pointer/data/script.js')
    pointer_js_code = pointer_js_file.read()
    pointer_js_file.close()
    return pointer_js_code


def injectScript() -> str:
    with open(f'{BASE_DIR}/pointer/data/inject.js') as injectJsFile:
        injectScriptCode = injectJsFile.read()
        return injectScriptCode


def makePointer() -> str:

    extension_dir = os.path.normpath(tempfile.mkdtemp())

    manifestTransformation_content = manifestTransformation()
    pointerTransformation_content = pointerTransformation()
    injectScript_content = injectScript()


    manifest_file = os.path.join(extension_dir, "manifest.json")
    with open(manifest_file, mode="w") as f:
        f.write(manifestTransformation_content)

    platform_file = os.path.join(extension_dir, "script.js")
    with open(platform_file, mode="w") as f:
        f.write(pointerTransformation_content)

    webGL_file = os.path.join(extension_dir, "inject.js")
    with open(webGL_file, mode="w") as f:
        f.write(injectScript_content)


    return extension_dir
