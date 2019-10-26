#!/usr/bin/env python
from os import environ
import re
import requests
import subprocess
from urllib.parse import urlparse, urlunparse, urljoin
from tempfile import mkstemp

environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

def run(cmd):
    args = cmd.split(' ')
    return subprocess.run(args, capture_output=True, check=True, text=True)

def api_get(api_url, resource, *args):
    url = urljoin(api_url, resource)
    for arg in args:
        url = urljoin(url + '/', arg)

    return requests.get(url, headers = { 'Private-Token': environ['GITLAB_TOKEN'] }).json()

def get_vars(api_url, resource, resource_id):
    result = {}
    variables = api_get(api_url, resource, str(resource_id), 'variables')
    for var in variables:
        if var['variable_type'] == 'env_var':
            result[var['key']] = var['value']
        if var['variable_type'] == 'file':
            fd, path = mkstemp()
            with open(path, 'w') as f:
                f.write(var['value'])
                result[var['key']] = path
    return result

def main():
    result = {}
    branch = run('git branch --show-current').stdout.rstrip()
    remote = run('git config --get branch.{0}.remote'.format(branch)).stdout.rstrip()
    remote_url = run('git config --get remote.{0}.url'.format(remote)).stdout.rstrip()
    remote_url_obj = urlparse(remote_url)
    api_url = urlunparse((remote_url_obj.scheme, remote_url_obj.netloc, "/api/v4/", None, None, None))

    match = re.match('^/([^/]+)/([^/]+)/?$', remote_url_obj.path)
    if not match:
        raise ValueError("Cannot parse GitLab URL")
    group_path = match.group(1)
    project_path = match.group(2)

    groups = api_get(api_url, 'groups')
    for group in groups:
        if group['path'] == group_path:
            result = {**result, **get_vars(api_url, 'groups', group['id'])}
    
    projects = api_get(api_url, 'projects')
    for project in projects:
        if project['path_with_namespace'] == '/'.join([group_path, project_path]):
            result = {**result, **get_vars(api_url, 'projects', project['id'])}

    for key, value in result.items():
        print("{0}={1}".format(key, value))
