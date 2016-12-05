#!/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import os
from email.mime.image import MIMEImage
import yaml
import shutil
from datetime import datetime
import logging
import commands
from random import shuffle
import argparse

# Loading configuration file (yaml->dict)
with open('config.yaml', 'r') as confile:
    Config = yaml.load(confile)

# Checking testing framework path existence
if not os.path.isdir(Config['testing_framework']['path']):
    raise Exception('Testing framework path doesn\'t exist: {}'.format(
        Config['testing_framework']['path']))

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def exec_cmd(cmd):
    out = commands.getoutput(cmd)
    print out
    logging.info(out)


class CMreserveJob(object):

    def __init__(self):

        self._email_addr = 'gshefer@redhat.com'
        self._test_framework = Config['testing_framework']['path']
        self._container_tests_path = os.path.join(self._test_framework,
                                                  'cfme/tests/containers')

    def _send_report(self):

        # Sending report to the receivers defined in configuration file

        if not os.path.exists(self._log_dir):
            raise Exception('Log directory doesn\'t exist: {}'.format(
                            self._log_dir))

        receivers = Config['reports']['daily']['receivers']

        msg = MIMEMultipart()
        msg['From'] = self._email_addr
        msg['To'] = COMMASPACE.join(receivers)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = Config['reports']['daily']['message']['subject']

        msg.attach(MIMEText(Config['reports']['daily']['message']['body']))

        for p in os.listdir(self._log_dir):

            fp = os.path.join(self._log_dir, p)
            ext = os.path.splitext(fp)[1]

            if ext in ('.png', '.jpeg', '.jpg'):
                with open(fp, 'rb') as fl:
                    data = MIMEImage(fl.read(), ext,
                                     name=os.path.basename(fp))
                msg.attach(data)

            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(self._email_addr, receivers, msg.as_string())

    def update_testing_framework(self):

        exec_cmd('cd {0}\ngit checkout master\ngit pull\n'.format(
                self._test_framework))

        shutil.copy('capture_container_dashboard.py',
                    os.path.join(self._test_framework, 'scripts',
                                 'capture_container_dashboard.py'))

    def _init_logs(self):

        # initiate log directory and files

        now = datetime.now()
        self._log_dir = '{}/log/{}-{}-{}_{}-{}-{}'.format(
            ROOT_PATH,
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        print 'Creating log directory: {}'.format(self._log_dir)
        os.makedirs(self._log_dir)
        self._log_path = os.path.join(self._log_dir, 'log.log')
        logging.basicConfig(filename=self._log_path, level=logging.DEBUG)

    def run(self, tests=0, report=False):

        # tests:  number of tests to run
        # report: whether to  send a report

        assert tests or report

        self._init_logs()
        self.update_testing_framework()

        test_script_path = os.path.join(os.getcwd(), '_temp_.bash')

        with open(test_script_path, 'w') as script:
            script.write('cd {}\n'.format(self._test_framework))

            if tests:

                itr = 0
                lst_dir = os.listdir(self._container_tests_path)
                shuffle(lst_dir)
                for p in lst_dir[:tests+1]:
                    if p.startswith('test_') and p.endswith('.py'):
                        ln = 'py.test --use-provider container {}\n'.format(
                            os.path.join(self._container_tests_path, p))
                        script.write(ln)
                        itr += 1
            if report:
                script.write('python {} {}\n'.format(
                    os.path.join(self._test_framework, 'scripts',
                                 'capture_container_dashboard.py'),
                    self._log_dir
                    ))

        exec_cmd('bash {}'.format(test_script_path))
        os.remove(test_script_path)

        if report:
            self._send_report()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='CM reserve options: ')
    parser.add_argument('--report', default=False, action='store_true',
                        help='report (Bool) whether to send a report or not')
    parser.add_argument('--tests', type=int, default=1,
                        help='Number of tests to execute (random)')

    args = parser.parse_args()

    CMreserveJob().run(report=args.report, tests=args.tests)
