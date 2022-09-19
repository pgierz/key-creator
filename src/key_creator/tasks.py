#!/usr/bin/env python3
"""
Basic tasks for generating a keypair, signing that keypair with a certificate,
and uploading the relevant keys to the login nodes of AWI's HPC system.

Provides the following functions and ``invoke`` CLI commands:
    * ``generate_keypair`` as a function (or ``generate-keypair`` as a CLI
      command)
    * ``sign_keypair_with_ca`` as a function (or ``sign-keypair-with-ca`` as a
      CLI command)
    * ``upload_keypair_to_login_node`` as a function (or
      ``upload-keypair-to-login-node`` as a CLI command)

For the command line version, you may use::
    
    $ inv <COMMAND>

Where ``<COMMAND>`` is one of the three commands given above. See the function
documentation for further information on each command.
"""
from invoke import task

from key_creator.upload_keypair import deploy_key

import os
import getpass

@task
def generate_keypair(c, key_suffix="_jupyterhub_hpc"):
    """
    Creates a Private/Public ssh keypair for use with the AWI HPC Jupyterhub

    Parameters
    ----------
    key_suffix : str
        A suffix which can be appended to the key to keep it unique from the
        default ``ssh-keygen`` name of ``id_rsa``. If no argument is supplied,
        defaults to ``jupyterhub_hpc``.
    """
    c.run(
        f"ssh-keygen -t rsa -f {os.environ['HOME']}/.ssh/id_rsa{key_suffix} -q -N ''"
    )


@task(pre=[generate_keypair])
def sign_keypair_with_ca(c, key_suffix="_jupyterhub_hpc"):
    """
    Signs the Private/Public ssh keypair with the certificate authority (ca)
    maintained at paleosrv3.dmawi.de as an extra layer of security.

    Parameters
    ----------
    key_suffix : str
        A suffix which can be appended to the key to keep it unique from the
        default `ssh-keygen` name of `id_rsa`. If no argument is supplied,
        defaults to `jupyterhub_hpc`
    """
    c.run(
        f"ssh-keygen -s /etc/ssh/ca -I {os.environ['USER']}@ollie0.awi.de -n {os.environ['USER']} {os.environ['HOME']}/.ssh/id_rsa{key_suffix}.pub"
    )


# FIXME(PG): I do not like that I need to pass the password as a plain text
# command flag. This should be different...
@task(help={"password": "Your password for the AWI's HPC Login Nodes"}, pre=[generate_keypair])
def upload_keypair_to_login_node(c, password=None, key_suffix="_jupyterhub_hpc"):
    """
    Uploads the key to a login node for future passwordless ssh access.

    Parameters
    ----------
    key_suffix : str
        A suffix which can be appended to the key to keep it unique from the
        default `ssh-keygen` name of `id_rsa`. If no argument is supplied,
        defaults to `jupyterhub_hpc`
    password : str
        Your AWI HPC Login password, in plain text. Defaults to ``None``, and
        in this case will prompt you to supply it via the command line.
    """
    key = open(f"{os.environ['HOME']}/.ssh/id_rsa{key_suffix}.pub").read()
    if password is None:
        password = getpass.getpass("Please enter your password for ollie0.awi.de: ")
    deploy_key(key, "ollie0.awi.de", os.environ["USER"], password)
