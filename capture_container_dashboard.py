from cfme.fixtures import pytest_selenium as sel
import base64
import argparse
import os


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
    scrn, _ = sel.take_screenshot()
    with open(ss_path, 'wb') as f:
        f.write(base64.b64decode(scrn))

if __name__ == '__main__':
    main()
