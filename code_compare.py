#! /usr/bin/python3
"""
./code_compare.py -l /Users/ternence/Workspace/idea/uat-r001/webull-trade-basic -r /Users/ternence/Workspace/idea/uat/webull-trade-basic
@Author: Ternence <xyancywong@outlook.com>
@Time: 2021/3/30 10:05
"""
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--left", default="", help="left source")
parser.add_argument("-r", "--right", default="", help="right source")
args = parser.parse_args()


codes = [
    "@TaskConsumer",
    "@KafkaListener",
    "@Value"
]

suffix = ".java"


def error(msg):
    print("\u001b[1;91m"+msg+"\u001b[0m")


def info(msg):
    print("\u001b[1;92m"+msg+"\u001b[0m")


def scan_file(base, file, res):
    f = open(file)
    pure_path = file.replace(base, "")
    for line in f.readlines():
        striped = line.strip()
        for code in codes:
            if code in striped and not striped.startswith("//"):
                if pure_path not in res:
                    res[pure_path] = []
                res[pure_path].append(striped)
                break


def scan_dir(base, pat, res):
    for file in os.listdir(pat):
        abs_path = pat+"/"+file
        if os.path.isdir(abs_path):
            scan_dir(base, abs_path, res)
        elif os.path.isfile(abs_path) and file.endswith(suffix):
            scan_file(base, abs_path, res)


def compare_one_file(base, lef, rig):
    sorted_lef = sorted(lef)
    sorted_rig = sorted(rig)
    cur_lef = 0
    cur_rig = 0
    while cur_lef < len(sorted_lef) and cur_rig < len(sorted_rig):
        if sorted_lef[cur_lef] == sorted_rig[cur_rig]:
            # print("same")
            cur_lef = cur_lef + 1
            cur_rig = cur_rig + 1
        elif sorted_lef[cur_lef] < sorted_rig[cur_rig]:
            print("left: (" + base + ") " + sorted_lef[cur_lef])
            cur_lef = cur_lef + 1
        else:
            print("right: (" + base + ") " + sorted_rig[cur_rig])
            cur_rig = cur_rig + 1

    while cur_lef < len(sorted_lef):
        print("left: (" + base + ") " + sorted_lef[cur_lef])
        cur_lef = cur_lef + 1
    while cur_rig < len(sorted_rig):
        print("right: (" + base + ") " + sorted_rig[cur_rig])
        cur_rig = cur_rig + 1


if not os.path.isdir(args.left):
    error(args.left + " not a dir!(left)")
    exit(1)

if not os.path.isdir(args.right):
    error(args.right + " not a dir!(right)")
    exit(1)

info("start compare " + args.left + " with " + args.right)

left = {}
right = {}

scan_dir(args.left, args.left, left)
scan_dir(args.right, args.right, right)

left_sorted_keys = sorted(left.keys())
right_sorted_keys = sorted(right.keys())

cur_left = 0
cur_right = 0
while cur_left<len(left_sorted_keys) and cur_right<len(right_sorted_keys):
    if left_sorted_keys[cur_left] == right_sorted_keys[cur_right]:
        compare_one_file(left_sorted_keys[cur_left], left[left_sorted_keys[cur_left]], right[right_sorted_keys[cur_right]])
        cur_left = cur_left + 1
        cur_right = cur_right + 1
    elif left_sorted_keys[cur_left] < right_sorted_keys[cur_right]:
        compare_one_file(left_sorted_keys[cur_left], left[left_sorted_keys[cur_left]], [])
        cur_left = cur_left + 1
    else:
        compare_one_file(right_sorted_keys[cur_right], [], right[right_sorted_keys[cur_right]])
        cur_right = cur_right + 1

while cur_left<len(left_sorted_keys):
    compare_one_file(left_sorted_keys[cur_left], left[left_sorted_keys[cur_left]], [])
    cur_left = cur_left + 1

while cur_right<len(right_sorted_keys):
    compare_one_file(right_sorted_keys[cur_right], [], right[right_sorted_keys[cur_right]])
    cur_right = cur_right + 1

