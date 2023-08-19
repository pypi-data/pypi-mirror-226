from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from polyrepo.gitlab import GitLab


def mockpost(responses):
    output = Mock()
    output.json = Mock(side_effect=responses)
    output.status_code = 200
    mock = Mock(return_value=output)
    return patch('polyrepo.gitlab.post', mock)


class TestGitLab(TestCase):

    def test_subgroups(self):
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
        with mockpost([r]):
            g = GitLab()
            x = g.groups('a')
            self.assertEqual(x, ['a', 'a/b', 'a/c'])
