# coding: utf-8

"""
    Test django_tools.unittest_utils.django_command
"""

import os
import sys
from unittest import TestCase

# https://github.com/jedie/django-tools
import django_tools
from django_tools.unittest_utils.django_command import DjangoCommandMixin

PY35 = sys.version_info[0:2] == (3, 5)

MANAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(django_tools.__file__), ".."))


class TestDjangoCommand(DjangoCommandMixin, TestCase):
    def test_help(self):
        output = self.call_manage_py(["--help"], manage_dir=MANAGE_DIR)

        self.assertNotIn("ERROR", output)
        self.assertIn("[django]", output)
        self.assertIn("Type 'manage.py help <subcommand>' for help on a specific subcommand.", output)

    def test_check(self):
        output = self.call_manage_py(["check"], manage_dir=MANAGE_DIR)
        self.assertNotIn("ERROR", output)
        self.assertIn("System check identified no issues (0 silenced).", output)

    def test_set_env(self):
        """
        Test if we can set "DJANGO_SETTINGS_MODULE"
        """
        env = dict(os.environ)
        env["DJANGO_SETTINGS_MODULE"]="does-not-exist"

        with self.assertRaises(AssertionError) as cm:
            self.call_manage_py(["--help"], manage_dir=MANAGE_DIR, env=env)

        output = "\n".join(cm.exception.args)
        # print(output)

        self.assertIn("subprocess exist status == 1", output)

        if PY35:
            member = "ImportError: No module named 'does-not-exist'"
        else:
            member = "ModuleNotFoundError: No module named 'does-not-exist'"

        self.assertIn(member, output)
