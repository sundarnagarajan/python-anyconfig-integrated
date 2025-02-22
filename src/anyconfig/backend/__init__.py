#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# Suppress import positions after some global variables are defined
# pylint: disable=wrong-import-position
"""A collection of backend modules available by default."""
import warnings

from . import (
    ini,
    json,
    pickle,
    properties,
    shellvars,
    yaml,
    xml
)
from .base import (
    ParserT, ParsersT, ParserClssT
)


PARSERS: ParserClssT = [
    ini.Parser, pickle.Parser, properties.Parser, shellvars.Parser, xml.Parser
] + json.PARSERS

_NA_MSG = "'{}' module is not available. Disabled {} support."

if yaml.PARSERS:
    PARSERS.extend(yaml.PARSERS)
else:
    warnings.warn(_NA_MSG.format('yaml', 'YAML'), ImportWarning)

try:
    from . import toml
    PARSERS.append(toml.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('toml', 'TOML'), ImportWarning)

try:
    from . import configobj
    PARSERS.append(configobj.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('configobj', 'ConfigObj'), ImportWarning)

try:
    from . import json5
    PARSERS.append(json5.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('json5', 'JSON5'), ImportWarning)

try:
    from . import bson
    PARSERS.append(bson.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('bson', 'BSON'), ImportWarning)

try:
    from . import cbor2
    PARSERS.append(cbor2.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('cbor2', 'CBOR2'), ImportWarning)

try:
    from . import msgpack
    PARSERS.append(msgpack.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('msgpack', 'MSGPACK'), ImportWarning)

try:
    from . import ion
    PARSERS.append(ion.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('ion', 'ION'), ImportWarning)


__all__ = [
    'ParserT', 'ParsersT', 'ParserClssT',
    'PARSERS',
]

# vim:sw=4:ts=4:et:
