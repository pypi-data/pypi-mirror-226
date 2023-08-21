import pdb
import unittest
from click.testing import CliRunner
from unittest.mock import patch
from io import StringIO
from dakka.cli import list_profiles, list_specs
from dakka.utils import write_config


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.config = {
            "openai_key": "test_key",
            "default_config": "default",
            "profiles": {
                "spec1": {"info": {"title": "spec1"}},
                "spec2": {"info": {"title": "spec2"}},
                "spec3": {"info": {"title": "spec3"}},
            },
            "configs": {
                "default": {
                    "enabled_specs": [
                        "spec1",
                        "spec2",
                    ]
                },
                "profile2": {
                    "enabled_specs": [
                        "spec3"
                    ]
                }
            }
        }
        write_config(self.config)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_configs(self, mock_stdout):
        runner = CliRunner()
        result = runner.invoke(list_profiles)
        self.assertEqual(result.output.strip(), "Available configurations: default, profile2")

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_specs_default(self, mock_stdout):
        runner = CliRunner()
        result = runner.invoke(list_specs, ["--profile", "default"])
        self.assertEqual(result.output.strip(), "Installed specs for config 'default': spec1, spec2")

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_specs_profile2(self, mock_stdout):
        runner = CliRunner()
        result = runner.invoke(list_specs, ["--profile", "config2"])
        self.assertEqual(result.output.strip(), "Installed specs for config 'config2': spec3")