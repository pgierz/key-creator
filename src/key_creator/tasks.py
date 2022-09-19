from invoke import task, Responder

import os


@task
def generate_keypair(c):
    c.run(
        f"ssh-keygen -t rsa -f {os.environ['HOME']}/.ssh/id_rsa_jupyterhub_hpc -q -N ''"
    )


@task
def sign_keypair_with_ca(c):
    c.run(
        f"ssh-keygen -s /etc/ssh/ca -I {os.environ['USER']}@ollie0.awi.de -n {os.environ['USER']} {os.environ['HOME']}/.ssh/id_rsa_jupyterhub_hpc.pub"
    )


@task
def upload_keypair_to_login_node(c, password):
    responder = Responder(
        pattern=f"{os.environ['USER']}@ollie0.awi.de's password: ",
        response=f"{password}\n",
    )
    c.run(
        f"ssh-copy-id -i {os.environ['HOME']}/.ssh/id_rsa_jupyterhub_hpc {os.environ['USER']}@ollie0.awi.de",
        watchers=[
            responder,
        ],
    )
