#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=broad-except
"""Utilities for anyconfig.cli.*.
"""
import typing

from .. import api, parser
from . import utils

if typing.TYPE_CHECKING:
    import argparse


def do_filter(cnf: typing.Dict[str, typing.Any], args: 'argparse.Namespace'):
    """Filter ``cnf`` by query/get/set and return filtered result.
    """
    if args.query:
        try:
            return api.try_query(cnf, args.query)
        except (Exception, ) as exc:
            utils.exit_with_output(f'Failed to query: exc={exc!s}', 1)

    if args.get:
        (cnf, err) = api.get(cnf, args.get)
        if cnf is None:
            utils.exit_with_output(f'Failed to get result: err={err!s}', 1)

        return cnf

    if args.set:
        (key, val) = args.set.split('=')
        api.set_(cnf, key, parser.parse(val))

    return cnf

# vim:sw=4:ts=4:et:
