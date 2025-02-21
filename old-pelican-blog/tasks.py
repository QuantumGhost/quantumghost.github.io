# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime
import pathlib
from string import Template

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

CONFIG = {
    # Local path configuration (can be absolute or relative to tasks.py)
    "deploy_path": "output",
    # Github Pages configuration
    "github_pages_branch": "master",
    "commit_message": "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    "port": 8000,
}


@task
def format(c):
    """format codes with formatters"""
    c.run("black .")


@task(name="check-style")
def check_style(c):
    c.run("black --check .")


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])
    c.run("find . -name '*.pyc' -delete")
    c.run("find . -name '__pycache__' -delete")


@task
def build(c):
    """Build local version of site"""
    c.run("pelican -s pelicanconf.py")


@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run("pelican -d -s pelicanconf.py")


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    c.run("pelican -r -s pelicanconf.py")


@task
def serve(c):
    """Serve site at http://localhost:8000/"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"], ("", CONFIG["port"]), ComplexHTTPRequestHandler
    )

    sys.stderr.write("Serving on port {port} ...\n".format(**CONFIG))
    server.serve_forever()


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    c.run("pelican -s publishconf.py")


@task
def publish(c):
    """Publish to GitHub Pages"""
    preview(c)
    c.run(
        "ghp-import -b {github_pages_branch} "
        "-m {commit_message} "
        "{deploy_path} -p".format(**CONFIG)
    )


@task
def watch(c):
    """Serve site at http://localhost:8000/ and watch for changes"""
    c.run("pelican -r -l -s pelicanconf.py")


@task(name="list-drafts")
def list_drafts(c):
    c.run("find . -name '*.draft'")


TMPL = """$title
=====================================================

:date: $date
:slug: $slug
:status: draft
:tags:
:category:


"""


@task
def new(c, slug, title=""):
    today = datetime.date.today()
    template = Template(TMPL)
    content = template.substitute(date=today.isoformat(), title=title, slug=slug)
    path = pathlib.Path(__file__).parent.joinpath("content", "drafts", f"{slug}.rst")
    if path.exists():
        print("file exists.")
        exit(1)

    with open(path, "w") as fout:
        fout.write(content)
