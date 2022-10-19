#!/usr/bin/env python3
"""
A small Flask app to generate SSH Keys via REST API requests

The following routes are available, sorted by HTTP request method:
    * ``GET``:
        * ``/``: Checks if the server is online and lists all possible routes
        * ``/generate_keypair``: Creates a public and private SSH key for AWI's
          HPC Jupyerhub
        * ``/sign_keypair``: Signs the keypair with the SSH Certificate
          Authority maintained at Paleosrv3.dmawi.de
    * ``POST``:
        * ``/upload_keypair``: Body of the HTTP Request should contain your
          login password. Keys are then uploaded to the AWI HPC system.
"""
from . import tasks
import os

from invoke.context import Context
from flask import Flask, request

app = Flask(__name__)

CONTEXT = Context()


@app.route("/")
def index():
    rvalue = ["Web server for SSH key generation is alive!"]
    for endpoint in app.url_map.iter_rules():
        rvalue.append(str(endpoint))
    return rvalue


@app.route("/generate_keypair")
def generate_keypair():
    """Generates a keypair for AWI Jupyterhub on HPC"""
    tasks.generate_keypair(CONTEXT)
    return "Keypair Generated!"


@app.route("/sign_keypair")
def sign_keypair():
    """Signs a keypair with the CA for AWI Jupyterhub on HPC"""
    tasks.sign_keypair_with_ca(CONTEXT)
    return "Keypair signed!"


@app.route("/upload_keypair", methods=["POST"])
def upload_keypair():
    """Uploads the keypair for AWI Jupyterhub on HPC"""
    password = request.form["password"]
    tasks.upload_keypair_to_login_node(CONTEXT, password)
    return "Keypair uploaded!"


@app.route("/full_sshkey_prep", methods=["POST"])
def full_sshkey_prep():
    """Generates, signs, and uploads a keypair"""
    generate_keypair()
    sign_keypair()
    upload_keypair()
    return "Keypair generated, signed, and uploaded. All good to go!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
