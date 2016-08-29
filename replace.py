import os
import re
import sys
import csv
import argparse

def file_match(fname, pat, old, replace):
    try:
        f = open(fname, "rt")
    except IOError:
        return
    data = f.readlines()
    new_data = []
    f.close()
    found = False
    for i, line in enumerate(data):
        if pat.search(line):
            print("%s: %i: %s" % (fname, i+1, line))
            found = True
        line = line.replace(old, replace)
        new_data.append(line)
    if found:
        with open(fname, "w") as f:
            for line in new_data:
                f.write(line)

def grep(dir_name, s_pat, replace):
    pat = re.compile(s_pat)
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for fname in filenames:
            fullname = os.path.join(dirpath, fname)
            file_match(fullname, pat, s_pat, replace)

def sources(path):
    replaces = []
    with open("source_codes.csv") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            replaces.append((row[0], row[1]))
    for source in replaces:
        grep(path, source[0], source[1])

class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

#Check for command line
parser = Parser()
parser.add_argument(dest='input', help="Enter folder to search")
args = parser.parse_args()
sources(args.input)

