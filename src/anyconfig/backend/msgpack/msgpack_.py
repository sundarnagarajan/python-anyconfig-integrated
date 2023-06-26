#
# Copyright (C) 2015 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import msgpack; help(msgpack.Unpacker); help(msgpack.Packer)"
#
r"""MessagePack backend:

- Format to support: MessagePack, http://msgpack.org
- Requirements: msgpack-python, https://pypi.python.org/pypi/msgpack/
- Development Status :: 4 - Beta
- Limitations: None obvious
- Special options:

  - All options of msgpack.load{s,} and msgpack.dump{s,} except object_hook
    and file_like should work.

  - See also: https://pypi.python.org/pypi/msgpack/

Changelog:

    .. versionadded:: 0.0.11
"""
from __future__ import absolute_import

import sys
import msgpack
from .. import base
import anyconfig.backend.base
IS_PYTHON_3 = (sys.version_info.major == 3)

from base import to_method


class Parser(base.StringStreamFnParser,
             base.BinaryFilesMixin):
    """
    Loader/Dumper for MessagePack files.
    """
    _type = "msgpack"
    # From https://github.com/msgpack/msgpack/issues/291
    _extensions = ['mpk', 'msgpack']
    _load_opts = ["read_size", "use_list", "object_hook", "list_hook",
                  "encoding", "unicode_errors", "max_buffer_size", "ext_hook",
                  "max_str_len", "max_bin_len", "max_array_len", "max_map_len",
                  "max_ext_len", "object_pairs_hook"]
    _dump_opts = ["default", "encoding", "unicode_errors", "use_single_float",
                  "autoreset", "use_bin_type"]
    _ordered = not anyconfig.compat.IS_PYTHON_3  # TODO.
    _dict_opts = ["object_pairs_hook"]  # Exclusive with object_hook

    _load_from_string_fn = to_method(msgpack.unpackb)
    _load_from_stream_fn = to_method(msgpack.unpack)
    _dump_to_string_fn = to_method(msgpack.packb)
    _dump_to_stream_fn = to_method(msgpack.pack)

# vim:sw=4:ts=4:et:
