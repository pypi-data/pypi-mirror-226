import os
from unittest.mock import patch
from pathlib import Path
from unittest import TestCase

from wizlib.command_handler import CommandHandler
from polyrepo.command import PolyRepoCommand
from polyrepo.command.groups_command import GroupsCommand
from test.test_gitlab import mockpost
from test import nohome
from test import patchconfig


@nohome()
class TestCommandGroups(TestCase):

    def test_from_handler(self):
        r = {
            "data": {
                "group": {
                    "descendantGroups": {
                        "nodes": [
                            {
                                "fullPath": "a/b"
                            },
                            {
                                "fullPath": "a/c"
                            }
                        ],
                        "pageInfo": {
                            "hasNextPage": False
                        }
                    }
                }
            }
        }
        with patchconfig():
            with mockpost([r]):
                r, s = CommandHandler(PolyRepoCommand).handle(['groups', 'a'])
                self.assertEqual(r, 'a\na/b\na/c')
