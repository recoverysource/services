#!/usr/bin/env python3
'''
Generate data for nginx
'''


def make_map(data, path='/etc/nginx/canonical_redirects.map'):
    '''
    Create an nginx map file from source data
    '''
    with open(path, 'w') as fh:
        for subdomain, meta in data.items():
            # Do not consider lists
            if not isinstance(meta['target'], str):
                continue
            nstype, nstarget = meta['target'].lower().split('^')
            # Only add domain "forwards" to nginx map
            if nstype != 'forward':
                continue
            # Append line for external redirect
            fh.write(f'{subdomain}.sober.page\t{nstarget};\n')
