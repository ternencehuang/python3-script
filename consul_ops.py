#! /usr/local/bin/python3
"""
save or load consul kvs
@Author: Ternence <xyancywong@outlook.com>
@Time: 2020/11/9 20:40
"""
import os
import argparse
import json
from consul_kv import Connection

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="load of save")
parser.add_argument("-c", "--consul", default="http://localhost:8500/v1/", help="consul address")
parser.add_argument("-f", "--force", action="store_true", help="force save")
parser.add_argument("-d", "--destination", default="/etc/xyancywong/consul/config_save", help="force save")
args = parser.parse_args()

conn = Connection(endpoint=args.consul)


def error(msg):
    print("\u001b[1;91m"+msg+"\u001b[0m")


def warn(msg):
    print("\u001b[1;93m"+msg+"\u001b[0m")


def info(msg):
    print("\u001b[1;92m"+msg+"\u001b[0m")


if args.mode == "save":
    exists = os.path.exists(args.destination)
    if exists:
        warn(args.destination + " already exist...")
        if args.force:
            warn("force rewrite save file...")
        else:
            warn("if you want save force pls add -f")
            exit(0)
    else:
        dirPath = os.path.dirname(args.destination)
        if os.path.exists(dirPath) and not os.path.isdir(dirPath):
            error(dirPath + " is not a dir")
        elif not os.path.exists(dirPath):
            os.makedirs(dirPath)
    info("start save kvs...")
    all_kvs = conn.get('', recurse=True)
    with open(args.destination, "w") as f:
        f.write(json.dumps(all_kvs))
    for kv in all_kvs:
        print("save kv: " + kv)
    info("end save kvs...")
elif args.mode == "load":
    exists = os.path.exists(args.destination)
    if not exists:
        error("can not found config file: " + args.destination)
        exit(0)
    info("start load kvs...")
    with open(args.destination) as f:
        kvs = json.loads(f.read())
        for kv in kvs:
            print("load kv: " + kv)
            conn.put(kv, kvs[kv])
    info("end save kvs...")
else:
    error("unavailable mode")
