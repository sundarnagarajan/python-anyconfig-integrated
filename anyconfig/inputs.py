#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=invalid-name
r"""Value objects represent inputs.

.. versionadded:: 0.9.5

- Add to make input object holding some attributes like input type (path,
  stream or pathlib.Path object), path, opener, etc.
"""
from __future__ import absolute_import

import collections
import anyconfig.utils

from anyconfig.globals import UnknownFileTypeError, UnknownParserTypeError


Input = collections.namedtuple("Input", "src type path parser opener".split())
ITYPES = (NONE, PATH_STR, PATH_OBJ, STREAM) = (None, "path", "pathlib.Path",
                                               "stream")


def guess_input_type(input_):
    """Guess input type of ``input_``.

    :param input_:
        Input object may be string (path), pathlib.Path object or (file) stream
    :return: Input type, NONE | PATH_STR | PATH_OBJ | STREAM

    >>> apath = "/path/to/a_conf.ext"
    >>> assert guess_input_type(apath) == PATH_STR

    >>> from anyconfig.compat import pathlib
    >>> if pathlib is not None:
    ...     assert guess_input_type(pathlib.Path(apath)) == PATH_OBJ
    >>> assert guess_input_type(open(__file__)) == STREAM
    """
    if input_ is None:
        return NONE
    elif anyconfig.utils.is_path(input_):
        return PATH_STR
    elif anyconfig.utils.is_path_obj(input_):
        return PATH_OBJ

    return STREAM


def _inspect_input(input_):
    """
    :param input_:
        Input object may be string (path), pathlib.Path object or (file) stream

    :return: A tuple of (input_type, input_path, input_opener)
    :raises: UnknownFileTypeError

    >>> import os.path

    >>> ipath_0 = os.path.join(os.path.dirname(__file__), "..",
    ...                        "tests/00-cnf.json")
    >>> ipath_1 = anyconfig.utils.normpath(ipath_0)

    >>> assert _inspect_input(ipath_0) == (PATH_STR, ipath_1, open)
    >>> assert _inspect_input(open(ipath_0)) == (STREAM, ipath_1,
    ...                                         anyconfig.utils.noop)
    >>> from anyconfig.compat import pathlib
    >>> if pathlib is not None:
    ...     ipo = pathlib.Path(ipath_0)
    ...     x = _inspect_input(ipo)
    ...     assert x == (PATH_OBJ, ipath_1, ipo.open)
    """
    itype = guess_input_type(input_)

    if itype == PATH_STR:
        ipath = anyconfig.utils.normpath(input_)
        opener = open
    elif itype == PATH_OBJ:
        ipath = anyconfig.utils.normpath(input_.as_posix())
        opener = input_.open
    elif itype == STREAM:
        ipath = anyconfig.utils.get_path_from_stream(input_)
        opener = anyconfig.utils.noop
    elif itype == NONE:
        ipath = None
        opener = anyconfig.utils.noop
    else:
        raise UnknownFileTypeError("%r" % input_)

    return (itype, ipath, opener)


def find_by_fileext(fileext, cps_by_ext):
    """
    :param fileext: File extension
    :param cps_by_ext: A list of pairs (file_extension, [parser_class])

    :return: Most appropriate parser class to process given file

    >>> from anyconfig.backends import _PARSERS_BY_EXT as cps
    >>> find_by_fileext("json", cps)
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_fileext("ext_should_not_be_found", cps) is None
    True
    """
    return next((psrs[-1] for ext, psrs in cps_by_ext if ext == fileext),
                None)


def find_by_filepath(filepath, cps_by_ext):
    """
    :param filepath: Path to the file to find out parser to process it
    :param cps_by_ext: A list of pairs (file_extension, [parser_class])

    :return: Most appropriate parser class to process given file

    >>> from anyconfig.backends import _PARSERS_BY_EXT as cps
    >>> find_by_filepath("/a/b/c/x.json", cps)
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_filepath("/path/to/a.ext_should_not_be_found", cps) is None
    True
    """
    fileext = anyconfig.utils.get_file_extension(filepath)
    return find_by_fileext(fileext, cps_by_ext)


def find_by_type(cptype, cps_by_type):
    """
    :param cptype: Config file's type
    :param cps_by_type: A list of pairs (parser_type, [parser_class])

    :return: Most appropriate parser class to process given type or None

    >>> from anyconfig.backends import _PARSERS_BY_TYPE as cps
    >>> find_by_type("json", cps)
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_type("missing_type", cps) is None
    True
    """
    return next((psrs[-1] or None for t, psrs in cps_by_type if t == cptype),
                None)


def find_parser(ipath, cps_by_ext, cps_by_type, forced_type=None):
    """
    :param ipath: Input file path
    :param cps_by_ext: A list of pairs (file_extension, [parser_class])
    :param cps_by_type: A list of pairs (parser_type, [parser_class])
    :param forced_type: Forced configuration parser type or parser object

    :return: Instance of parser class appropriate for the input `ipath`
    :raises: ValueError, UnknownParserTypeError, UnknownFileTypeError

    >>> from anyconfig.backends import (
    ...      _PARSERS_BY_EXT as cps_by_ext,
    ...      _PARSERS_BY_TYPE as cps_by_type
    ... )
    >>> cpss = (cps_by_ext, cps_by_type)

    >>> find_parser(None, cps_by_ext, cps_by_type,
    ...             forced_type="type_not_exist"
    ...             )  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    UnknownParserTypeError: No parser found for type 'type_not_exist'
    >>> find_parser("cnf.ext_not_found", *cpss
    ...             )  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    UnknownFileTypeError: No parser found for file 'cnf.ext_not_found'

    >>> isinstance(find_parser(None, cps_by_ext, cps_by_type,
    ...                        forced_type="ini"),
    ...            anyconfig.backend.ini.Parser)
    True
    >>> isinstance(find_parser("cnf.json", *cpss),
    ...            anyconfig.backend.json.Parser)
    True
    >>> isinstance(find_parser("cnf.json", cps_by_ext, cps_by_type,
    ...                        forced_type="json"),
    ...            anyconfig.backend.json.Parser)
    True
    """
    if (ipath is None or not ipath) and forced_type is None:
        raise ValueError("ipath or forced_type must be some value")

    if forced_type is None:
        parser = find_by_filepath(ipath, cps_by_ext)
        if parser is None:
            raise UnknownFileTypeError(ipath)

        return parser()

    if isinstance(forced_type, anyconfig.backend.base.Parser):
        return forced_type

    parser = find_by_type(forced_type, cps_by_type)
    if parser is None:
        raise UnknownParserTypeError(forced_type)

    return parser()


def make(input_, cps_by_ext, cps_by_type, forced_type=None):
    """
    :param input_:
        Input object which may be string (path), pathlib.Path object or (file)
        stream object
    :param cps_by_ext: A list of pairs (file_extension, [parser_class])
    :param cps_by_type: A list of pairs (parser_type, [parser_class])
    :param forced_type: Forced configuration parser type

    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownParserTypeError, UnknownFileTypeError

    >>> from anyconfig.backends import (
    ...      _PARSERS_BY_EXT as cps_by_ext,
    ...      _PARSERS_BY_TYPE as cps_by_type
    ... )
    >>> cpss = (cps_by_ext, cps_by_type)

    >>> make(None, *cpss)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: input_ or forced_type must be some value

    >>> from anyconfig.compat import pathlib
    >>> if pathlib is not None:
    ...     path = pathlib.Path("/path/to/cnf.json")
    ...     x = make(path, *cpss)
    ...     assert isinstance(x.parser, anyconfig.backend.json.Parser)
    ...     assert x.path == "/path/to/cnf.json"
    """
    if (input_ is None or not input_) and forced_type is None:
        raise ValueError("input_ or forced_type must be some value")

    (itype, ipath, opener) = _inspect_input(input_)
    psr = find_parser(ipath, cps_by_ext, cps_by_type, forced_type=forced_type)

    return Input(src=input_, type=itype, path=ipath, parser=psr, opener=opener)

# vim:sw=4:ts=4:et:
