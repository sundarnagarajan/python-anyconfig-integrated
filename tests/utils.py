#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2019 - 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""test cases for anyconfig.utils.
"""
import pathlib
import unittest

import anyconfig.ioinfo
import anyconfig.utils as TT

import tests.common


class Test(unittest.TestCase):

    def test_00_get_file_extension(self):
        self.assertEqual(TT.get_file_extension("/a/b/c"), '')
        self.assertEqual(TT.get_file_extension("/a/b.txt"), "txt")
        self.assertEqual(TT.get_file_extension("/a/b/c.tar.xz"), "xz")


class TestCaseWithWorkdir(tests.common.TestCaseWithWorkdir):

    def test_10_expand_paths(self):
        fun = TT.expand_paths

        tdir = self.workdir / "a" / "b" / "c"
        tdir.mkdir(parents=True)

        pathlib.Path(tdir / 'd.txt').touch()
        pathlib.Path(tdir / 'e.txt').touch()
        pathlib.Path(tdir / 'f.json').write_text("{'a': 1}\n")

        # single path:
        path = tdir / 'd.txt'
        self.assertEqual(fun(str(path)), [path])
        self.assertEqual(fun(path), [path])
        with path.open() as fobj:
            self.assertEqual(fun(fobj), [fobj])
        self.assertEqual(fun(anyconfig.ioinfo.make(path)), [path])

        # single path contains a glob pattern:
        self.assertEqual(fun(tdir / '*.txt'),
                         [tdir / 'd.txt', tdir / 'e.txt'])
        self.assertEqual(fun(tdir.parent / '**' / '*.txt'),
                         [tdir / 'd.txt', tdir / 'e.txt'])
        self.assertEqual(fun(tdir.parent / '**' / '*.*'),
                         [tdir / 'd.txt', tdir / 'e.txt', tdir / 'f.json'])

        # multiple paths:
        self.assertEqual(fun([tdir / 'e.txt', tdir / 'd.txt']),
                         [tdir / 'd.txt', tdir / 'e.txt'])

# vim:sw=4:ts=4:et:
