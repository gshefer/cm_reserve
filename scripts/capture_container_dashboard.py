import argparse
import os
from cfme.fixtures import pytest_selenium as sel
from utils.browser import WithZoom
from inter_utils import save_screenshot


def save_screenshot_entire_overview(path):

    base = os.path.splitext(path)[0]
    cap1p, cap2p = (base+'_0.png', base+'_1.png')
    save_screenshot(cap1p)
    elem = sel.element('//div[contains(@head-title,'
                       ' "Pod Creation and Deletion Trends")]')
    sel.move_to_element(elem)
    save_screenshot(cap2p)


@WithZoom(2)
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
