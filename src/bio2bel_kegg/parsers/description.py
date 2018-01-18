# -*- coding: utf-8 -*-

"""
This module parsers the description files -> http://rest.kegg.jp/get/ in KEGG RESTful API

"""

import re

import requests

from bio2bel_kegg.constants import API_KEGG_GET


def parse_entry_line(line):
    """ Parse entry line to tuple

    :param line:
    :rtype tuple
    :return: tuple of entry
    """
    return tuple(
        [line.strip(' ')
         for line in line.split()[1:]
         ]
    )


def remove_first_word(string):
    """ Remove the first word of the line

    :param str string: string
    :rtype str
    :return: string without the first word
    """
    return string.split(' ', 1)[1].strip()


def get_first_word(string):
    """ Get the first word of the line

    :param str string: string
    :rtype str
    :return: string with the first word
    """
    return string.split(' ', 1)[0]


def parse_pathway_line(line):
    """ Parse entry pathway line to tuple

    :param line:
    :rtype tuple
    :return: tuple of entry
    """

    line = remove_first_word(line)

    return tuple(
        [line.strip(' ')
         for line in re.split(r'\s{2,}', line)
         ]
    )


def parse_link_line(line):
    """ Parse entry dblink line to tuple

    :param line:
    :rtype tuple
    :return: tuple of entry
    """

    line = remove_first_word(line)

    return tuple(
        [line.strip(' ')
         for line in re.split(r'\s{2,}', line)
         ]
    )


def parse_description(identifier):
    """ Parse the description file of the identifier using the KEGG API

    :param str identifier: id for the query
    :rtype: dict
    :return: description dictionary
    """

    r = requests.get(API_KEGG_GET.format(identifier), stream=True)

    description = {}

    for line in r.iter_lines():
        line = line.decode('utf-8')

        if not line.startswith(' '):
            keyword = get_first_word(line)

        if keyword == 'ENTRY':
            description['ENTRY'] = parse_entry_line(line)

        elif keyword == 'PATHWAY':

            if 'PATHWAY' not in description:
                description['PATHWAY'] = [parse_pathway_line(line)]
            else:
                description['PATHWAY'].append(parse_pathway_line(line))

        elif keyword == 'DBLINKS':

            if 'DBLINKS' not in description:
                description['DBLINKS'] = [parse_link_line(line)]
            else:
                description['DBLINKS'].append(parse_link_line(line))

    return description


if __name__ == '__main__':
    description = parse_description('hsa:5214')
    print(description)