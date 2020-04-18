#!/usr/bin/env python

import argparse
import logging
import subprocess as sp
from io import StringIO
import re


class ParseError(Exception):
    def __init__(self, ex, act):
        super(ParseError, self).__init__(ex, act)


class UnexpectedLine(ParseError):
    pass


def name(lines):
    if lines[0][0] == "+":
        return 1
    else:
        raise UnexpectedLine("line beginning with '+'", lines[0])


def open_paren(lines):
    if lines[0][0] == "{":
        return 1
    else:
        raise UnexpectedLine("{", lines[0])


def close_paren(lines):
    if lines[0][0] == "}":
        return 1
    else:
        raise UnexpectedLine("}", lines[0])


def attribute(lines, obj):
    m = re.match(r'^"(.+)" = (.+)', lines[0])
    if m:
        v = re.sub(r'^"?([^"]+)"?$', r"\1", m[2])
        obj[m[1]] = v
        return 1
    else:
        raise UnexpectedLine('"key" = value', lines[0])


def object_(lines, ls):
    pos = 0
    pos += name(lines[pos:])
    pos += open_paren(lines[pos:])
    obj = {}
    while lines[pos][0] != "}":
        pos += attribute(lines[pos:], obj)
    pos += close_paren(lines[pos:])
    ls.append(obj)
    return pos


def parse(s):
    ret = []
    lines = [l.strip() for l in s.split("\n") if len(l.strip()) > 0]
    pos = 0
    while pos < len(lines):
        pos += object_(lines[pos:], ret)
    return ret


def check1(obj):
    if int(obj["BatteryPercent"]) >= 10:
        return ""
    return "{}: Battery is low ({})\n".format(
        obj["Product"],
        obj["BatteryPercent"]
    )


def check(ls):
    msg = []
    for obj in ls:
        ret = check1(obj)
        if len(ret) > 0:
            msg.append(ret)
    return "\n".join(msg)


def alert(msg):
    sp.run([
        "osascript",
        "-e",
        f'display alert "{msg}"'
    ])


def main(args):
    ret = sp.run([
        "ioreg",
        "-lr",
        "-k",
        "BatteryPercent"
    ], stdout=sp.PIPE)
    s = ret.stdout.decode("utf-8")
    objs = parse(s)
    msg = check(objs)
    if len(msg) > 0:
        alert(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    logging.basicConfig(
        filename="check.log",
        level=logging.DEBUG,
        format="[%(levelname)s]%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main(args)
