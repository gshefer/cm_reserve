import base64
from cfme.fixtures import pytest_selenium as sel


def save_screenshot(path):

    scrn, _ = sel.take_screenshot()
    with open(path, 'wb') as f:
        f.write(base64.b64decode(scrn))
