#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
import yaml
import json
import sys

parser = ArgumentParser()
parser.add_argument('infile', nargs='?', type=FileType('r'), default=sys.stdin)
args = parser.parse_args()

# with open("test.yaml", 'r') as stream:

with args.infile as stream:
    try:
        print("---")
        for data in yaml.load_all(stream):
            j = json.dumps(data, indent=2)
            print(j)
            print("---")
    except yaml.YAMLError as exc:
        print(exc)

