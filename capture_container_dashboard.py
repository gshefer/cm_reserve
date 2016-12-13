from cfme.fixtures import pytest_selenium as sel
import base64
import argparse
import os
from utils.browser import browser
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
import time


def save_screenshot_entire_overview(path):

    AC = ActionChains(browser())
    AC.send_keys(keys.Keys.CONTROL, keys.Keys.ADD)
    for _ in xrange(5):
        AC.perform()
    time.sleep(2)
    base = os.path.splitext(path)[0]
    cap1p, cap2p = (base+'_0.png', base+'_1.png')
    scrn, _ = sel.take_screenshot()
    with open(cap1p, 'wb') as f:
        f.write(base64.b64decode(scrn))
    elem = sel.element('//div[contains(@head-title,'
                       ' "Pod Creation and Deletion Trends")]')
    sel.move_to_element(elem)
    time.sleep(2)
    scrn, _ = sel.take_screenshot()
    with open(cap2p, 'wb') as f:
        f.write(base64.b64decode(scrn))


def main():

    # Capture a screenshot of container dashboard (Containers->Overview)

    fmtr = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(epilog=__doc__,
                                     formatter_class=fmtr)
    parser.add_argument('log_dir_path', type=str,
                        help='The path of the log directory')

    args = parser.parse_args()

    if not os.path.isdir(args.log_dir_path):
        raise Exception('No such directory: {}'.format(args.log_dir_path))

    sel.force_navigate('container_dashboard')
    ss_path = '{}/container_dashboard.png'.format(args.log_dir_path)
    save_screenshot_entire_overview(ss_path)

if __name__ == '__main__':
    main()
