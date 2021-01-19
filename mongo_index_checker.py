#! /usr/bin/python3
"""
python3 mongo_index_checker.py -s mongodb://localhost:27017/core -d mongodb://localhost:27017/aws

using for check mongo index between two dbs
@Author: Ternence <xyancywong@outlook.com>
@Time: 2021/1/18 23:02
"""
import argparse
import pymongo


def get_db(uri):
    parts = uri.split("/")
    return parts[len(parts)-1]


def compare_index(x, y):
    xkey = x["key"]
    ykey = y["key"]

    xkeys = xkey.keys()
    ykeys = ykey.keys()

    if len(xkeys) != len(ykeys):
        return False

    for i in range(len(xkeys)):
        if xkeys[i] != ykeys[i]:
            return False
        if xkey[xkeys[i]] * ykey[ykeys[i]] <= 0:
            return False

    return True


def self_index(index):
    keys = index["key"].keys()
    if len(keys) == 1 and keys[0] == "_id":
        return True
    return False


def generate_cmd(col, index, index_names):
    seq = 0
    name = "ix_" + str(seq)
    seq = seq + 1
    while name in index_names:
        name = "ix_" + str(seq)
        seq = seq + 1
    index_names.append(name)

    cmd = "db.getCollection(\"" + col + "\").createIndex({"
    keys = index["key"]
    fir = True
    for key in keys.keys():
        if fir:
            fir = False
        else:
            cmd = cmd + ","
        cmd = cmd + "\"" + key + "\":" + str(int(keys[key]))
    cmd = cmd + "},{\"background\":true,\"name\":\"" + name + "\"})"
    return cmd


p = argparse.ArgumentParser()
p.add_argument("-s", "--source", default="", help="source mongo uri")
p.add_argument("-d", "--destination", default="", help="destination mongo uri")
args = p.parse_args()

source = pymongo.MongoClient(args.source)[get_db(uri=args.source)]
source_cols = source.list_collection_names(session=None)

destination = pymongo.MongoClient(args.destination)[get_db(uri=args.destination)]
destination_cols = destination.list_collection_names(session=None)

for col in source_cols:
    index_names = []
    for index in destination[col].list_indexes():
        index_names.append(index["name"])

    first = True
    for index in source[col].list_indexes():
        already_have = False
        for des_index in destination[col].list_indexes():
            if_same = compare_index(index, des_index)
            if if_same:
                already_have = True

        if not already_have and not self_index(index):
            if first:
                first = False
            print(generate_cmd(col, index, index_names))

