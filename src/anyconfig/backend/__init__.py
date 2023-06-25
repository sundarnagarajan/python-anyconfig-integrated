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


__all__ = [
    'ParserT', 'ParsersT', 'ParserClssT',
    'PARSERS',
]

# vim:sw=4:ts=4:et:
