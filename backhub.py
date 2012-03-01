#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import argparse
import base64
import json
import getpass
import logging
import os
import pprint
import subprocess
import urllib.error
import urllib.request

# http://developer.github.com/v3/repos/
API_URL = 'https://api.github.com/user/repos?type=%s'

def clone(user, passwd, type, ssh, directory):
    request = urllib.request.Request(url=API_URL % type)

    credentials = base64.b64encode(('%s:%s' % (user, passwd)).encode('utf-8'))
    request.add_header('Authorization', 'Basic %s' % credentials.decode('ascii'))

    response = urllib.request.urlopen(request)

    raw_json = response.read()
    repos = json.loads(raw_json.decode('utf-8'))

    oldpwd = os.getcwd()
    os.chdir(directory)

    with open(os.devnull, 'w') as devnull:
        for i, repo in enumerate(repos, start=1):
            name = repo['name']
            clone_url = repo['ssh_url'] if ssh else repo['clone_url']
            logging.info('%3d/%3d - Cloning %s', i, len(repos), name)
            ret = subprocess.call(['git', 'clone', clone_url],
                                  stdout=devnull, stderr=devnull)

            if ret != 0:
                logging.error('Error cloning %s (%s)', name, clone_url)

    os.chdir(oldpwd)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Clone all your Github repos.')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--pass', dest='passwd')
    parser.add_argument('-t', '--type', default='all',
                        choices=['all', 'owner', 'public', 'private', 'member'],
                        help='Which type of repos needs to be cloned.')
    parser.add_argument('--https', default=True, action='store_false',
                        dest='ssh',
                        help='Clone via https (ssh by default).')
    parser.add_argument('-d', '--directory', default='.',
                        help='In which directory the repos should be cloned '
                        '(. by default).')

    args = parser.parse_args()

    if not args.user:
        args.user = input('Username: ')

    if not args.passwd:
        args.passwd = getpass.getpass()

    try:
        clone(args.user, args.passwd, args.type, args.ssh, args.directory)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            logging.error('Wrong user/passwd')
        else:
            logging.error(e)
    except Exception as e:
        logging.error(e)

