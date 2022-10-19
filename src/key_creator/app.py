#!/usr/bin/env python3
"""
A small Flask app to generate SSH Keys via REST API requests

.. qrefflask:: key_creator.app:app

.. autoflask:: key_creator.app:app
   :endpoints:
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
