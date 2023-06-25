#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2019 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=too-many-ancestors
r"""CBOR backend:

- Format to support: CBOR, http://cbor.io, https://tools.ietf.org/html/rfc7049
- Requirements: cbor2, https://pypi.python.org/pypi/cbor2
- Development Status :: 3 - Alpha
- Limitations: None obvious
- Special options:

  - All options of cbor2.load{s,} and cbor2.dump{s,} should work.
  - See also: https://github.com/agronholm/cbor2/blob/master/cbor2/

Changelog:
.. versionchanged:: 0.0.4

   - enhancement: add _cid to allow users to chose this than cbor explicitely

.. versionchanged:: 0.0.3

   - fix: follow internal API changes of the argument for load/dump functions

.. versionadded:: 0.0.2
"""
from __future__ import absolute_import

import cbor2
from .. import base
from base import to_method


class Parser(base.StringStreamFnParser,
             base.BinaryFilesMixin):
    """Parser for CBOR files.
    """
    _type = "cbor"
    _cid = "cbor2"
    _priority = 10  # Gives higher precedence than cbor.
    _extensions = ["cbor"]
    _loads_opts = ["tag_hook", "object_hook"]
    _dump_opts = ["datetime_as_timestamp", "timezone", "value_sharing",
                  "default"]

    _load_from_string_fn = to_method(cbor2.loads)
    _load_from_stream_fn = to_method(cbor2.load)
    _dump_to_string_fn = to_method(cbor2.dumps)
    _dump_to_stream_fn = to_method(cbor2.dump)

# vim:sw=4:ts=4:et:
