from __future__ import print_function

from click.testing import CliRunner
import json
from mock import patch, call
import requests
import unittest
import uuid

from bergenholmclient.scripts import cli as cli_mod
from bergenholmclient.scripts.cli import cli

UUID = str(uuid.uuid4())
GROUP = 'group1'
TEMPLATE = 'temp1'

HEADERS = {
    'Content-Type': 'application/json'
}


class HostSubcommandTestCase(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    # Host subcommand test cases

    @patch('requests.get')
    def test_host_list(self, patched):
        self.runner.invoke(cli, ['host', 'list'])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/hosts/', auth=None)])

    @patch('requests.get')
    def test_host_show(self, patched):
        self.runner.invoke(cli, ['host', 'show', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/hosts/' + UUID, auth=None)])

    @patch('requests.get')
    def test_host_show_all(self, patched):
        self.runner.invoke(cli, ['host', 'show', '--all', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/hosts/%s?params=all' % UUID,
                 auth=None)])

    @patch('requests.post')
    def test_host_create(self, patched):
        self.runner.invoke(cli, ['host', 'create', UUID,
                                 'tests/sample_host.json'])
        with open('tests/sample_host.json') as f:
            data = f.read()
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/hosts/' + UUID,
                 data=data, headers=HEADERS, auth=None)])

    @patch('requests.put')
    def test_host_update(self, patched):
        self.runner.invoke(cli, ['host', 'update', UUID,
                                 'tests/sample_host.json'])
        with open('tests/sample_host.json') as f:
            data = f.read()
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/hosts/' + UUID,
                 data=data, headers=HEADERS, auth=None)])

    @patch('requests.delete')
    def test_host_delete(self, patched):
        self.runner.invoke(cli, ['host', 'delete', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/hosts/' + UUID, auth=None)])

    # Group subcommand test cases

    @patch('requests.get')
    def test_group_list(self, patched):
        self.runner.invoke(cli, ['group', 'list'])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/groups/', auth=None)])

    @patch('requests.get')
    def test_group_show(self, patched):
        self.runner.invoke(cli, ['group', 'show', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/groups/' + UUID, auth=None)])

    @patch('requests.get')
    def test_group_show_all(self, patched):
        self.runner.invoke(cli, ['group', 'show', '--all', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/groups/%s?params=all' % UUID,
                 auth=None)])

    @patch('requests.post')
    def test_group_create(self, patched):
        self.runner.invoke(cli, ['group', 'create', UUID,
                                 'tests/sample_group.json'])
        with open('tests/sample_group.json') as f:
            data = f.read()
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/groups/' + UUID,
                 data=data, headers=HEADERS, auth=None)])

    @patch('requests.put')
    def test_group_update(self, patched):
        self.runner.invoke(cli, ['group', 'update', UUID,
                                 'tests/sample_group.json'])
        with open('tests/sample_group.json') as f:
            data = f.read()
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/groups/' + UUID,
                 data=data, headers=HEADERS, auth=None)])

    @patch('requests.delete')
    def test_group_delete(self, patched):
        self.runner.invoke(cli, ['group', 'delete', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/groups/' + UUID, auth=None)])

    # template subcommand test cases

    @patch('requests.get')
    def test_template_list(self, patched):
        self.runner.invoke(cli, ['template', 'list'])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/templates/', auth=None)])

    @patch('requests.get')
    def test_template_show(self, patched):
        self.runner.invoke(cli, ['template', 'show', TEMPLATE])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/templates/' + TEMPLATE, auth=None)])

    @patch('requests.get')
    def test_template_show_all(self, patched):
        self.runner.invoke(cli, ['template', 'show', TEMPLATE, '--host', UUID])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/templates/%s/%s' % (
                 TEMPLATE, UUID), auth=None)])

    @patch('requests.post')
    def test_template_create(self, patched):
        self.runner.invoke(cli, ['template', 'create', TEMPLATE,
                                 'tests/sample_template.txt'])
        with open('tests/sample_template.txt') as f:
            data = f.read()
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/templates/' + TEMPLATE,
                 data=data, headers=HEADERS, auth=None)])

    @patch('requests.put')
    def test_template_update(self, patched):
        self.runner.invoke(cli, ['template', 'update', TEMPLATE,
                                 'tests/sample_template.txt'])
        with open('tests/sample_template.txt') as f:
            data = f.read()
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/templates/' + TEMPLATE,
                 data=data, headers=HEADERS, auth=None)])

    @patch('requests.delete')
    def test_template_delete(self, patched):
        self.runner.invoke(cli, ['template', 'delete', TEMPLATE])
        patched.assert_has_calls([
            call('http://127.0.0.1/api/1.0/templates/' + TEMPLATE, auth=None)])
