from cfme.fixtures import pytest_selenium as sel
import base64
import argparse
import os
from utils.browser import browser
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from cfme.intelligence.reports.reports import CannedSavedReport


def save_screenshot(path):

    AC = ActionChains(browser())
    AC.send_keys(keys.Keys.CONTROL, keys.Keys.SUBTRACT)
    for _ in xrange(3):
        AC.perform()
    time.sleep(2)
    scrn, _ = sel.take_screenshot()
    with open(path, 'wb') as f:
        f.write(base64.b64decode(scrn))


def main():

    # Capture a screenshot of the produced chargeback1_fixedrate report.

    fmtr = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(epilog=__doc__,
                                     formatter_class=fmtr)
    parser.add_argument('log_dir_path', type=str,
                        help='The path of the log directory')

    args = parser.parse_args()

    if not os.path.isdir(args.log_dir_path):
        raise Exception('No such directory: {}'.format(args.log_dir_path))

    path_to_report = ['My Company (All EVM Groups)',
                      'Custom', 'Chargeback1-FixedRate']
    run_at = CannedSavedReport.queue_canned_report(path_to_report)
    report = CannedSavedReport(path_to_report, run_at)
    report.navigate()
    ss_path = '{}/chargeback_fixedrate_report.png'.format(args.log_dir_path)
    save_screenshot(ss_path)


if __name__ == '__main__':
    main()
