#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

__author__ = "Janell.Huyck and madarp"

import sys
import re
import argparse

if sys.version_info[0] >= 3:
    raise Exception("This program requires python2 interpreter")

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract the year and print it
 - Extract the names and rank numbers and just print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a single
    list starting with the year string followed by the name-rank
    strings in alphabetical order. ['2006', 'Aaliyah 91', Aaron 57',
     'Abagail 895', ' ...]"""
    names = []
    file_data = extract_file_data(filename)
    name_year = str(
        re.search(r'Popularity\sin\s(\d\d\d\d)', file_data).group(1))
    name_dict = extract_name_dict(file_data)
    names.append(name_year)
    for name in sorted(name_dict):
        name_pair = str(name + " " + name_dict[name])
        names.append(name_pair)
    return names


def extract_file_data(filename):
    with open(filename, "r") as f:
        file_data = f.read()
    return file_data


def extract_name_dict(file_data):
    name_dict = {}
    names = re.findall(
        r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', file_data)
    for ranked_name in names:
        if ranked_name[1] not in name_dict:
            name_dict[ranked_name[1]] = ranked_name[0]
        if ranked_name[2] not in name_dict:
            name_dict[ranked_name[2]] = ranked_name[0]
    return name_dict


def create_parser():
    """Create a cmd line parser object with 2 argument definitions"""

    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more filenames.
    # It will also expand wildcards just like the shell, e.g.
    # 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    create_summary = ns.summaryfile  # option flag

    for file in file_list:
        name_list = extract_names(file)

        if create_summary:
            filename = "{}.summary".format(file)
            with open(filename, "w") as summary_file:
                summary_file.write('\n'.join(name_list))
        else:
            print('\n'.join(name_list))


if __name__ == '__main__':
    main(sys.argv[1:])
