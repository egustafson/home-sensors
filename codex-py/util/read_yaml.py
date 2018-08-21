#!/usr/bin/env python3

import yaml
import json

with open("test.yaml", 'r') as stream:
    try:
        data = yaml.load(stream)
        j = json.dumps(data, indent=2)
        print(j)
    except yaml.YAMLError as exc:
        print(exc)

