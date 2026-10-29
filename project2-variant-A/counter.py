#!/usr/bin/env python3

import sys

filename = sys.argv[1]

with open(filename, "r") as file:
    lines = file.readlines()

print(len(lines))

