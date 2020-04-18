#!/usr/bin/env python

import argparse
import logging
import re
from jinja2 import Template, Environment, FileSystemLoader
import os
import subprocess as sp


def pwd():
    ret = sp.run(["pwd"], stdout=sp.PIPE)
    return ret.stdout.decode("utf-8").strip()


def python():
    ret = sp.run(["which", "python"], stdout=sp.PIPE)
    return ret.stdout.decode("utf-8").strip()


def main(args):
    env = Environment(loader=FileSystemLoader("."), trim_blocks=False)
    ret = env.get_template(args.file).render(dict(
        pwd=pwd(),
        python=python()
    ))
    print(ret)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    logging.basicConfig(
        filename="render.log",
        level=logging.DEBUG,
        format="[%(levelname)s]%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main(args)
