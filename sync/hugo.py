#!/usr/bin/env python3
'''
Load data from hugo
'''
import glob
import os
import yaml


def load_yaml(fpath='data/domains.yaml'):
    '''
    Returns an object from a yaml file (or directory of yaml files)
    '''
    fpath = fpath.rstrip('/')

    # if fpath is a file
    if os.path.isfile(fpath):
        return yaml.load(
                open(fpath, 'r', encoding='utf-8'),
                Loader=yaml.SafeLoader)

    # if fpath is a directory when .yaml is removed
    if not os.path.isdir(fpath) and os.path.isdir(fpath.rstrip('.yaml')):
        fpath = fpath.rstrip('.yaml')

    # if fpath a directory
    if os.path.isdir(fpath):
        m = {}
        for path in glob.glob(f'{fpath}/*'):
            if '.yaml' not in path:
                continue
            tag = path.replace(f'{fpath}/', '', 1).replace('.yaml', '')
            m[tag] = yaml.load(
                    open(path, 'r', encoding='utf-8'),
                    Loader=yaml.SafeLoader)
        return m

    raise Exception('Could not load yaml data')


def normalize(hugo_data):
    '''
    Returns a flattened form of hugo data **and** inject default values.
    '''
    # Flatten data structre
    normal_data = flatten_source(hugo_data)

    # Set default values
    for tag, data in normal_data.items():

        # [type]: forward OR cname
        if 'type' not in data:
            # Pages targets
            if any(s in data['target']
                   for s in [
                       'github.io',
                       'gitlab.io',
                       'pages.dev',
                       ]):
                data['type'] = 'cname'
            else:
                data['type'] = 'forward'

    # Return normalized data
    return normal_data


def flatten_source(original):
    '''
    Return dictionary with one key for each subdomain
    '''
    return {
            subk: subv
            for k, v in original.items() for subk, subv in v.items()}
