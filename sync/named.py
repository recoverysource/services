#!/usr/bin/env python3
'''
Generate zone file for bind9 (named)
'''


ZONE_TEMPLATE = '''\
; Bind9 data file for recovery source services
$TTL    86400
@       IN      SOA     service1 admin.sober.page. (
                              1         ; Serial
                           1800         ; Refresh
                           1800         ; Retry
                          86400         ; Expire
                           3600 )       ; Negative Cache TTL
; NS-1
@        IN      NS      service1
service1 IN      A       134.199.236.204
service1 IN      AAAA    2604:a880:4:1d0::cfaf:d000
; Default
*        IN      CNAME   service1
; Zone Data
'''


def make_zone(data, path):
    '''
    Create a bind9 zone file from source data
    '''
    with open(path, 'w') as fh:
        fh.write(ZONE_TEMPLATE)
        for subdomain, meta in data.items():
            # Cast string to list
            if isinstance(meta['target'], str):
                meta['target'] = [meta['target']]
            for target in meta['target']:
                nstype, nstarget = target.lower().split('^')
                dot = ''
                # Do not add domain "forwards" to DNS (handled by */nginx)
                if nstype == 'forward':
                    continue
                elif nstype == 'cname':
                    dot = '.'
                # Append line to name server
                fh.write(
                        f'{subdomain}\tIN\t{nstype.upper()}\t'
                        f'{nstarget.rstrip(".")}{dot}\n')
