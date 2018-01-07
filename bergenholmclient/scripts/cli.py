#from __future__ import print_function
import click
import os
import requests
from requests.auth import HTTPBasicAuth

import bergenholmclient

DEFAULT_URL = 'http://127.0.0.1/api/1.0'
HEADERS = {'Content-Type': 'application/json'}
PARAMS = '?params=all'
MARK_INSTALLED = "?installed=mark"
UNMARK_INSTALLED = "?installed=unmark"


def print_list(auth, url, key, query=None):
    result = requests.get(url, auth=auth, params=query)
    result.raise_for_status()
    entries = result.json().get(key, [])
    entries.sort()
    for entry in entries:
        print(entry)


def print_entry(auth, url):
    result = requests.get(url, auth=auth)
    result.raise_for_status()
    print(result.content)


def create_entry(auth, url, fd=None, data=None):
    if data is not None:
        result = requests.post(url, data=data, headers=HEADERS, auth=auth)
    elif fd is not None:
        result = requests.post(url, data=fd.read(), headers=HEADERS, auth=auth)
    result.raise_for_status()


def update_entry(auth, url, fd=None, data=None):
    if data is not None:
        result = requests.put(url, data=data, headers=HEADERS, auth=auth)
    elif fd is not None:
        result = requests.put(url, data=fd.read(), headers=HEADERS, auth=auth)
    result.raise_for_status()


def delete_entry(auth, url):
    result = requests.delete(url, auth=auth)
    result.raise_for_status()


@click.group()
@click.option('--url', metavar='URL',
              envvar='BERGENHOLM_URL', default=DEFAULT_URL,
              help='REST API URL ($BERGENHOLM_URL)')
@click.option('--user', metavar='USER',
              envvar='BERGENHOLM_USER', default=None,
              help='User name ($BERGENHOLM_USER)')
@click.option('--password', metavar='PASSWORD',
              envvar='BERGENHOLM_PASSWORD', default=None,
              help='Passowrd ($BERGENHOLM_PASSWORD)')
@click.pass_context
def cli(ctx, url, user, password):
    ctx.obj = {
        'URL': url,
        'AUTH': None,
        'HOST_URL': url + '/hosts/',
        'GROUP_URL': url + '/groups/',
        'TEMPLATE_URL': url + '/templates/',
        'POWER_URL': url + '/power/'
    }
    if user is not None and password is not None:
        ctx.obj['AUTH'] = HTTPBasicAuth('user', 'pass')


@cli.group('host', help='Host operations')
@click.pass_context
def host(ctx):
    pass


@cli.group('group', help='Group operations')
@click.pass_context
def group(ctx):
    pass


@cli.group('template', help='Template operations')
@click.pass_context
def template(ctx):
    pass


@cli.group('power', help='Power operations')
@click.pass_context
def power(ctx):
    pass


@host.command('list', help='List uuids of host')
@click.option('--query', '-q', multiple=True,
              help='Query condition')
@click.pass_context
def get_hosts(ctx, query):
    query_dict = {}
    for entry in query:
        if "=" in entry:
            key, value = entry.split('=', 1)
        query_dict[key] = value
    print_list(ctx.obj['AUTH'], ctx.obj['HOST_URL'], 'hosts', query=query_dict)


@host.command('show', help='Show parameters of a host')
@click.argument('uuid')
@click.option('--all', is_flag=True,
              help='Include parameters from groups')
@click.pass_context
def get_host(ctx, uuid, all):
    if all:
        print_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid + PARAMS)
    else:
        print_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid)


@host.command('create', help='Register parameters of a host')
@click.argument('uuid')
@click.argument('jsonfile', type=click.File('rb'))
@click.pass_context
def create_host(ctx, uuid, jsonfile):
    create_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid, fd=jsonfile)


@host.command('update', help='Update parameters of a host')
@click.argument('uuid')
@click.argument('jsonfile', type=click.File('rb'))
@click.pass_context
def update_host(ctx, uuid, jsonfile):
    update_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid, fd=jsonfile)


@host.command('mark-installed', help='Register parameters of a host')
@click.argument('uuid')
@click.pass_context
def mark_installed_host(ctx, uuid):
    print_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid + MARK_INSTALLED)


@host.command('unmark-installed', help='Register parameters of a host')
@click.argument('uuid')
@click.pass_context
def mark_uninstalled_host(ctx, uuid):
    print_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid + UNMARK_INSTALLED)


@host.command('delete', help='Remove parameters of a host')
@click.argument('uuid')
@click.pass_context
def delete_host(ctx, uuid):
    delete_entry(ctx.obj['AUTH'], ctx.obj['HOST_URL'] + uuid)


@group.command('list', help='List names of group')
@click.pass_context
def get_groups(ctx):
    print_list(ctx.obj['AUTH'], ctx.obj['GROUP_URL'], 'groups')


@group.command('show', help='Show parameters of a group')
@click.argument('name')
@click.option('--all', is_flag=True)
@click.pass_context
def get_group(ctx, name, all):
    if all:
        print_entry(ctx.obj['AUTH'], ctx.obj['GROUP_URL'] + name + PARAMS)
    else:
        print_entry(ctx.obj['AUTH'], ctx.obj['GROUP_URL'] + name)


@group.command('create', help='Register parameters of a group')
@click.argument('name')
@click.argument('jsonfile', type=click.File('rb'))
@click.pass_context
def create_group(ctx, name, jsonfile):
    create_entry(ctx.obj['AUTH'], ctx.obj['GROUP_URL'] + name, fd=jsonfile)


@group.command('update', help='Update parameters of a group')
@click.argument('name')
@click.argument('jsonfile', type=click.File('rb'))
@click.pass_context
def update_group(ctx, name, jsonfile):
    update_entry(ctx.obj['AUTH'], ctx.obj['GROUP_URL'] + name, fd=jsonfile)


@group.command('delete', help='Remove parameters of a group')
@click.argument('name')
@click.pass_context
def delete_group(ctx, name):
    delete_entry(ctx.obj['AUTH'], ctx.obj['GROUP_URL'] + name)


@template.command('list', help='List names of template')
@click.pass_context
def get_templates(ctx):
    print_list(ctx.obj['AUTH'], ctx.obj['TEMPLATE_URL'], 'templates')


@template.command('show', help='Show a template')
@click.argument('name')
@click.option('--host', metavar='UUID', default=None)
@click.pass_context
def get_template(ctx, name, host):
    if host:
        print_entry(ctx.obj['AUTH'],
                    ctx.obj['TEMPLATE_URL'] + name + '/' + host)
    else:
        print_entry(ctx.obj['AUTH'], ctx.obj['TEMPLATE_URL'] + name)


@template.command('create', help='Register a template')
@click.argument('name')
@click.argument('jsonfile', type=click.File('rb'))
@click.pass_context
def create_template(ctx, name, jsonfile):
    create_entry(ctx.obj['AUTH'], ctx.obj['TEMPLATE_URL'] + name, fd=jsonfile)


@template.command('update', help='Update a template')
@click.argument('name')
@click.argument('jsonfile', type=click.File('rb'))
@click.pass_context
def update_template(ctx, name, jsonfile):
    update_entry(ctx.obj['AUTH'], ctx.obj['TEMPLATE_URL'] + name, fd=jsonfile)


@template.command('delete', help='Remove a template')
@click.argument('name')
@click.pass_context
def delete_template(ctx, name):
    delete_entry(ctx.obj['AUTH'], ctx.obj['TEMPLATE_URL'] + name)


@power.command('on', help='Start a host')
@click.argument('uuid')
@click.pass_context
def power_on(ctx, uuid):
    mode = '{"power": "on"}'
    update_entry(ctx.obj['AUTH'], ctx.obj['POWER_URL'] + uuid, data=mode)


@power.command('off', help='Stop a host')
@click.argument('uuid')
@click.pass_context
def power_off(ctx, uuid):
    mode = '{"power": "off"}'
    update_entry(ctx.obj['AUTH'], ctx.obj['POWER_URL'] + uuid, data=mode)


@power.command('reset', help='Reset a host')
@click.argument('uuid')
@click.pass_context
def power_reset(ctx, uuid):
    mode = '{"power": "reset"}'
    update_entry(ctx.obj['AUTH'], ctx.obj['POWER_URL'] + uuid, data=mode)


@power.command('status', help='Show power status of a host')
@click.argument('uuid')
@click.pass_context
def get_power_status(ctx, uuid):
    print_entry(ctx.obj['AUTH'], ctx.obj['POWER_URL'] + uuid)


if __name__ == '__main__':
    cli(obj={})
