#!/usr/bin/env python3
'''
Synchronize data with CloudFlare
NOTE: Obsolete - CF has a 200/1k limit on DNS records, we need unlimited
'''
import configparser
import CloudFlare
import logging
import os


def push_dns(source_data, zone=None):
    '''
    Verify that source data is in sync with cloudflare DNS.
    '''
    cf = CloudFlare.CloudFlare()

    # Read zone from configuration if it was not provided
    if not zone:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.expanduser('~'), '.cloudflare.cfg'))
        zone = config['CloudFlare']['zone']

    # Get current records
    current_records = {}
    for record in cf.zones.dns_records.get(zone):
        # Skip unmanaged records
        if record.get('comment') != 'sync-managed':
            logging.debug(f'Skipping unmanaged record: {record["id"]}')
            continue
        current_records[record['name'].partition('.')[0]] = record

    # Pre-sync prune
    for subdomain, record in dict(current_records).items():
        rminfo = f'{record["name"]} {record["type"]} {record["content"]}'

        # Delete managed CF records no longer in source data
        if subdomain not in source_data:
            logging.warning(f'Deleting unmatch record: {rminfo}')
            cf.zones.dns_records.delete(zone, record['id'])

        # Delete forwards (handled by catch-all)
        elif source_data[subdomain]['type'].lower() == 'forward':
            logging.warning(f'Deleting forwarded record: {rminfo}')
            cf.zones.dns_records.delete(zone, record['id'])

        # Delete if type needs to change
        elif record['type'].upper() != source_data[subdomain]['type'].upper():
            logging.warning(f'Deleting record with wrong type: {rminfo}')
            cf.zones.dns_records.delete(zone, record['id'])
            del current_records[subdomain]

    # Verify expected records against current state
    for subdomain, record in source_data.items():
        # Forwards are handled by DNS catch-all
        if record['type'] == 'forward':
            continue

        # Create record if it does not exist
        elif subdomain not in current_records:
            logging.info(f'Creating record for {subdomain}')
            cf.zones.dns_records.post(zone, data={
                'type': record['type'].upper(),
                'name': f'{subdomain}.sober.page',
                'content': record['target'],
                'proxied': record.get('cache', False),
                'comment': 'sync-managed',
                })

        # Update record if current values are incorrect
        elif (record.get('cache') != current_records[subdomain]['proxied']
              or record['target'] != current_records[subdomain]['content']):
            logging.info(f'Updating record values for {subdomain}')
            cf.zones.dns_records.put(
                    zone, current_records[subdomain]['id'], data={
                        'type': record['type'].upper(),
                        'name': f'{subdomain}.sober.page',
                        'content': record['target'],
                        'proxied': record.get('cache', False),
                        'comment': 'sync-managed',
                        })
