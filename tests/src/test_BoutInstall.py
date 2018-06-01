#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import shutil
from pathlib import Path
from src.BoutInstall import BoutInstall


class TestBoutInstall(unittest.TestCase):
    def setUp(self):
        """
        Set up global test parameters
        """

        self.installer = BoutInstall()
        root_dir = Path(__file__).absolute().parents[2]
        self.main_dir = root_dir.joinpath('test_main_dir')
        self.other_dir = root_dir.joinpath('test_other_dir')

    def tearDown(self):
        """
        Remove created directories and files
        """

        shutil.rmtree(self.main_dir, ignore_errors=True)
        shutil.rmtree(self.other_dir, ignore_errors=True)

    def test_set_install_dirs(self):
        """
        Tests that the directories are properly installed
        """

        self.installer.set_install_dirs(main_dir=self.main_dir)
        install_dir = self.main_dir.joinpath('install')
        local_dir = self.main_dir.joinpath('local')
        examples_dir = self.main_dir.joinpath('examples')
        self.assertTrue(install_dir.is_dir())
        self.assertTrue(local_dir.is_dir())
        self.assertTrue(examples_dir.is_dir())

        install_dir = self.other_dir.joinpath('install')
        local_dir = self.other_dir.joinpath('local')
        examples_dir = self.other_dir.joinpath('examples')
        self.installer.set_install_dirs(install_dir=install_dir,
                                        local_dir=local_dir,
                                        examples_dir=examples_dir)
        self.assertTrue(install_dir.is_dir())
        self.assertTrue(local_dir.is_dir())
        self.assertTrue(examples_dir.is_dir())

    def test_get_tar_file(self):
        self.fail()

    def test_untar(self):
        self.fail()

    def test_configure(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
