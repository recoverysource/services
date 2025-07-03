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
            # Only consider domain forwards on this server.
            if meta['type'].lower() != 'forward':
                continue
            # Append line for external redirect
            fh.write(f'{subdomain}.sober.page\t{meta["target"]};\n')
