#!/usr/bin/python
import os
from getpass import getpass
import time

import paramiko


def deploy_key(key, server, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=username, password=password)
    stdin, stdout, stderr = client.exec_command("mkdir -p ~/.ssh/")
    stdout.readlines()
    stdin, stdout, stderr = client.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
    stdout.readlines()
    stdin, stdout, stderr = client.exec_command("chmod 644 ~/.ssh/authorized_keys")
    stdout.readlines()
    stdin, stdout, stderr = client.exec_command("chmod 700 ~/.ssh/")
    stdout.readlines()


def main():
    key = open(os.path.expanduser("~/.ssh/id_rsa.pub")).read()
    username = os.getlogin()
    password = getpass()
    hosts = ["hostname1", "hostname2", "hostname3"]
    for host in hosts:
        deploy_key(key, host, username, password)


if __name__ == "__main__":
    main()
